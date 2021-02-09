# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-25 19:14:37
lastTime: 2021-02-09 18:44:15
'''

import json
import os
import platform

def _load_config(path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, "r") as fp:
            globals().update(json.load(fp))
            print("Load configs:", path)

def _initialize():
    directory = os.path.dirname(__file__)
    sys_name = platform.system().lower()
    _load_config("{}/{}.json".format(directory, "shared"))
    _load_config("{}/{}.json".format(directory, sys_name))

_initialize()
