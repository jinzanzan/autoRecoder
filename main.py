#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    : main.py
@Time    : 2021/12/13 14:23:07
@Version : 0.1
@License : Apache License Version 2.0, January 2004
@Desc    : None
'''
import os

if __name__ == "__main__":
    latitude = ""
    longitude = ""
    mode = "debug"
    if mode != "debug":
        from yfd.yfd import Ydk
        if "latitude" in os.environ:
            latitude = os.environ["latitude"]
            longitude = os.environ["longitude"]
        config = {
            "accessToken": os.environ["accessToken"],
            "secret": os.environ["secret"],
            "latitude": latitude,
            "longitude": longitude,
            "province": os.environ["province"],
            "city": os.environ["city"],
            "area": os.environ["area"],
            "address": os.environ["address"]
        }
    else:
        from yfd.cdb import Ydk
        config = {}
    dk = Ydk(config)
    dk.create_table()
    # dk.submit()
