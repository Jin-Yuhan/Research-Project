# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-25 19:14:37
lastTime: 2021-02-13 20:26:33
'''

def load_configs():
    import assets
    import json
    import os
    import platform

    tags = {
        "asset": lambda v: assets.get_absolute_path(v),
        "platform": lambda v: v[platform.system().lower()]
    }

    paths = [
        assets.get_absolute_path("config.json")
    ]

    def handle_tags(configs):
        result = {}
        for k, v in configs.items():
            words = k.split(":")
            value = handle_tags(v) if isinstance(v, dict) else v
            for i in range(len(words) - 1):
                value = tags[words[i]](value)
            result[words[-1]] = value
        return result
    
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as fp:
                configs = json.load(fp)
                if isinstance(configs, dict):
                    globals().update(handle_tags(configs))
                    print("Load configs:", path)
                else:
                    print("Invalid configs:", path)
        else:
            print("Configs not found:", path)

load_configs()
del load_configs