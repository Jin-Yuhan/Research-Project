# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-25 19:14:14
lastTime: 2021-02-09 22:35:17
'''

import configs
import tfmodels
import random
import train_data as td

def main():
    data = td.load_at_path(configs.tfmodel_data["train_data_path"])

    if data:
        print("load %d train data" % len(data))
        random.shuffle(data)  # 随机排序一次
        model = tfmodels.TrainModel(**configs.tfmodel_common, **configs.tfmodel_train)
        model.train(data)
    else:
        print("No train data!")

if __name__ == "__main__":
    main()
