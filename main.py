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
from yfd.yfd import Ydk

if __name__ == "__main__":
    config = {
        "accessToken": os.environ["accessToken"],
        "secret": os.environ["secret"],
        "province": os.environ["province"],
        "city": os.environ["city"],
        "area": os.environ["area"],
        "address": os.environ["address"],
        "inschool": os.environ["inschool"],
        "isdes": os.environ["isdes"],
        "reason": os.environ["reason"],
        "reasondes": os.environ["reasondes"]
    }
    pzinfo = {
        "inschool": config["inschool"],
        "isdes": config["isdes"],
        "reason": config["reason"],
    }
    fillinfo = {
        "inschool": "",
        "isdes": "",
        "reason": config["reasondes"]
    }
    dk = Ydk(config, pzinfo, fillinfo)
    dk.submit()
