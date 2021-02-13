# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-25 19:14:14
lastTime: 2021-02-13 21:40:38
'''

import configs
import json
import os
import random
import tfmodels
from async_receiver import AsyncHumanDataReceiver

class ModelData(object):
    def __init__(self, path):
        self.path = path
        self.labeled_data_list = None

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, mode="r") as fp:
                obj = json.load(fp)
                if isinstance(obj, list):
                    self.labeled_data_list = obj
                    print("Load model data:", self.path)

    def save(self):
        if self.labeled_data_list:
            with open(self.path, mode="w") as fp:
                json.dump(self.labeled_data_list, fp)
                print("Save model data:", self.path)

    def get_batch(self, size=None):
        if not size:
            size = len(self)
            
        samples = random.sample(self.labeled_data_list, k=size)
        data = []
        labels = []

        for s in samples:
            value, label = ModelData.extract_labeled_data(s)
            data.append(value)
            labels.append(label)
        return data, labels

    def append(self, data, label):
        labeled_data = ModelData.mark_label_on_data(data, label)
        self.labeled_data_list.append(labeled_data)

    def __len__(self):
        return len(self.labeled_data_list)

    def __getitem__(self, index):
        return self.labeled_data_list[index]

    @staticmethod
    def mark_label_on_data(data, label):
        return [data, label]

    @staticmethod
    def extract_labeled_data(data):
        return data[0], data[1]

def make_data(data_path):
    model_data = ModelData(data_path)
    model_data.load()
    receiver = AsyncHumanDataReceiver(None, **configs.arduino)
    receiver.start()
    
    while receiver.active:
        try:
            value = int(input(">>> "))
        except ValueError:
            print("The input value must be an integer.")
            continue

        if value > 0 and value < 10:
            data = receiver.latest_data
            if data:
                label = [int(i == value) for i in range(1, 10)]
                model_data.append(data, label)
                print(model_data[-1])
        elif value == -1:
            break
        else:
            print("The input value must be in [1,9], or equal -1.")
    
    receiver.stop()
    model_data.save()
    saved_count = len(model_data)

    if saved_count > 0:
        print("%d Data saved!" % saved_count)
    else:
        print("Data save failed!")

def run_model(model_type, data_path, **kwargs):
    model_data = ModelData(data_path)
    model_data.load()
    
    if len(model_data) > 0:
        print("Load %d data" % len(model_data))
        random.shuffle(model_data.labeled_data_list)  # 随机排序一次
        model = model_type(**kwargs)
        model.run(model_data.get_batch)
    else:
        print("No data!")

def make_train_data():
    """Make Train Data."""
    make_data(configs.train_data_path)

def make_test_data():
    """Make Test Data."""
    make_data(configs.test_data_path)

def train_model():
    """Train Model."""
    run_model(
        tfmodels.TrainModel,
        configs.train_data_path,
        **configs.tfmodel_common,
        **configs.tfmodel_train
    )

def test_model():
    """Test Model."""
    run_model(
        tfmodels.TestModel,
        configs.test_data_path,
        **configs.tfmodel_common
    )

def quit():
    """Quit."""
    exit(0)

if __name__ == "__main__":
    modes = [
        make_train_data,
        make_test_data,
        train_model,
        test_model,
        quit
    ]

    while True:
        try:
            print("Select Mode:")
            for i in range(len(modes)):
                print("    %d.%s" % (i + 1, modes[i].__doc__))
            
            modes[int(input(">>> ")) - 1]()
        except Exception as e:
            print(e)
            continue
