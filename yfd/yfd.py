#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    : yfd.py
@Time    : 2021/12/13 16:35:31
@Version : 0.1
@License : Apache License Version 2.0, January 2004
@Desc    : None
'''
from abc import abstractproperty
import requests
import geocoder
import json
import datetime
from yfd.config import *
from math import radians, cos, sin, asin, sqrt


class Ydk(object):
    def __init__(self, config) -> None:
        super().__init__()
        self.index = "https://yfd.ly-sky.com/ly-pd-mb/form/api/healthCheckIn/client/stu/index"
        self.dk_url = "https://yfd.ly-sky.com/ly-pd-mb/form/api/answerSheet/saveNormal"
        self.headers = {
            "Host": "yfd.ly-sky.com",
            "Accept-Encoding": "gzip, deflate, br,compress",
            "userAuthType": "MS",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001030) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wx217628c7eb8ec43c/11/page-frame.html",
            "accessToken": config["accessToken"]
        }
        self.config = config
        self.secret = config["secret"]
        self.address = config["address"]
        self.province = self.config["province"]
        self.city = self.config["city"]
        self.area = self.config["area"]
        self.latitude = self.config["latitude"]
        self.longitude = self.config["longitude"]
        self.get_geo()

    def sendmess(self, title):
        r = requests.post(
            "https://sctapi.ftqq.com/{}.send".format(self.secret), data={"title": title})
        result = json.loads(r.text)
        return result

    def haversine(self, lon2, lat2):
        lon1 = 112.919075
        lat1 = 28.221294
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2-lon1
        dlat = lat2-lat2
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        c = 2*asin(sqrt(a))
        r = 6371
        return int(c*r*2000)

    def getDetailUrl(self):
        r = requests.get(self.index, headers=self.headers)
        result = json.loads(r.text)
        self.entityid = result["data"]["questionnairePublishEntityId"]
        self.ques_url = "https://yfd.ly-sky.com/ly-pd-mb/form/api/questionnairePublish/{}/getDetailWithAnswer".format(
            self.entityid)

    def getDetail(self):
        r = requests.get(self.ques_url, headers=self.headers)
        result = json.loads(r.text)
        self.ques_id = result["data"]["questionnairePublishFillVo"]["questionnairePublishEntityId"]
        self.start_time = int(
            result["data"]["questionnairePublishFillVo"]["fillStartTime"])
        self.end_time = int(
            result["data"]["questionnairePublishFillVo"]["fillEndTime"])
        self.had_fill = result["data"]["questionnairePublishFillVo"]["hadFill"]

    def get_geo(self):
        try:
            g = geocoder.arcgis(self.address)
            self.latitude, self.longitude = g.latlng
        except Exception as e:
            if self.latitude:
                pass
            else:
                self.latitude = 28.221294
                self.longitude = 112.919075

    def struct_ques(self):
        out = []
        for key in id_list.keys():
            if pzinfo[key]:
                out.append({
                    "subjectType": "signleSelect",
                    "subjectId": id_list[key],
                    "signleSelect": {
                        "fillContent": fillinfo[key],
                        "beSelectValue": reason_list[pzinfo[key]] if key == "reason" else pzinfo[key]
                    }
                })
        ques_list = [
            {
                "subjectType": "multiSelect",
                "subjectId": "1001635817858477001050000000001",
                "multiSelect": {
                    "optionAnswerList": [
                        {
                            "fillContent": "",
                            "beSelectValue": "NotThing"
                        }
                    ]
                }
            }, {
                "subjectType": "location",
                "subjectId": "1001635817858481001050000000001",
                "location": {
                    "latitude": self.latitude,
                    "longitude": self.longitude,
                    "province": self.province,
                    "deviationDistance": self.haversine(self.longitude, self.latitude),
                    "locationRangeId": "1001638329616882001070000000001",
                    "city": self.city,
                    "area": self.area,
                    "address": self.address
                }
            }
        ]
        self.ques_list = ques_list+out

    def submit(self):
        if "latitude" not in self.config:
            self.get_geo()
        self.struct_ques()
        try:
            tdtime = datetime.datetime.now()
            if tdtime.hour >= 0 and tdtime.hour < 15:
                self.getDetailUrl()
                self.getDetail()
                print(self.ques_list)
                if self.had_fill is False:
                    self.getDetailUrl()
                    data = {
                        "answerInfoList": self.ques_list,
                        "questionnairePublishEntityId": self.ques_id,
                    }
                    r = requests.post(
                        self.dk_url, headers=self.headers, json=data)
                    result = json.loads(r.text)
                    if result["code"] == 200:
                        print("打卡成功", result)
                        if self.secret:
                            self.sendmess("打卡成功")
                    else:
                        print("打卡失败", result)
                        if self.secret:
                            self.sendmess("打卡失败")
                else:
                    print("已经打过卡了")
            else:
                print("休息时间")
        except Exception as e:
            print("程序出错", e)
            if self.secret:
                self.sendmess("程序出错")
