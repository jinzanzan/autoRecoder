#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2022/01/08 11:02:10
@Author  :   aminkira
@Version :   1.0
@Contact :   aminkira2019@gmail.com
@Desc    :   None
'''
'''
inschool: 在学校的状态：
    1: 在学校
    2. 不在学校
isdes: 如果不在学校需要填写,如果在学校则不需要填写：
    1. 请假了
    2. 没有请假
reason: 没有请假的理由，如果在学校则不需要填写
    1. 已经办理校外租房
    2. 毕业生，已办理长假手续
    3. 已经办理校外实习手续
    4. 其他
'''
pzinfo = {
    "inschool": "2",
    "isdes": "2",
    "reason": "3",
}
fillinfo = {
    "inschool": "",
    "isdes": "",
    "reason": ""
}
id_list = {
    "inschool": "1001637746058450004920000000001",
    "isdes": "1001637746095542004980000000001",
    "reason": "1001638346284708001930000000001"
}
reason_list = {
    "1": "1",
    "2": "2",
    "3": "flag1638346253991",
    "4": "flag1638346272310"
}
