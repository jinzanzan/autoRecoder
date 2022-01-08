#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    : yfd.py
@Time    : 2021/12/13 16:35:31
@Version : 0.1
@License : Apache License Version 2.0, January 2004
@Desc    : None
'''
import requests
import geocoder
import json
import datetime


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
        self.get_geo()

    def sendmess(self, title):
        r = requests.post(
            "https://sctapi.ftqq.com/{}.send".format(self.secret), data={"title": title})
        result = json.loads(r.text)
        return result

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
            self.latitude = 28.221294
            self.longitude = 112.919075

    def struct_ques(self):
        if "湖南工商大学" not in self.address:
            out = [
                {
                    "subjectType": "signleSelect",
                    "subjectId": "1001637746058450004920000000001",
                    "signleSelect": {
                        "fillContent": "",
                        "beSelectValue": "2"
                    }
                }, {
                    "subjectType": "signleSelect",
                    "subjectId": "1001637746095542004980000000001",
                    "signleSelect": {
                        "fillContent": "",
                        "beSelectValue": "2"
                    }
                }, {
                    "subjectType": "signleSelect",
                    "subjectId": "1001638346284708001930000000001",
                    "signleSelect": {
                        "fillContent": "",
                        "beSelectValue": "flag1638346253991"
                    }
                }
            ]
        else:
            out = [{
                "subjectType": "signleSelect",
                "subjectId": "1001637746058450004920000000001",
                "signleSelect": {
                    "fillContent": "",
                    "beSelectValue": "1"
                }
            }]
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
                    "province": self.config["province"],
                    "deviationDistance": 281115,
                    "locationRangeId": "1001638329616882001070000000001",
                    "city":self.config["city"],
                    "area":self.config["area"],
                    "address":self.config["address"]
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
