# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-09 22:05:40
lastTime: 2021-02-09 22:38:46
'''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import configs
import tfmodels
import random
import train_data as td

def main():
    data = td.load_at_path(configs.tfmodel_data["test_data_path"])

    if data:
        print("load %d test data" % len(data))
        random.shuffle(data)  # 随机排序一次
        model = tfmodels.TestModel(**configs.tfmodel_common)
        model.test(data)
    else:
        print("No test data!")

if __name__ == "__main__":
    main()