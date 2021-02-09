# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-25 22:12:24
lastTime: 2021-02-09 18:38:13
'''

import json
import os
import random

def load_at_path(path):
    """读取指定路径下的训练数据。

    Args:
        path: 训练数据保存的路径。

    Returns:
        训练数据列表。如果没有在指定的路径下找到训练数据，返回一个空列表。
    """
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, mode="r") as fp:
            return json.load(fp)
    return []

def save_to_path(path, data):
    """将训练数据保存至指定路径。

    Args:
        path: 训练数据保存的路径。
        data: 训练数据，其类型必须为 list 或 tuple。

    Returns:
        保存的训练数据的个数。
        如果 data 的类型错误或者长度为0，则返回-1。
    """
    if isinstance(data, (list, tuple)) and data:
        last_data = load_at_path(path)
        if last_data:
            data.extend(last_data)  # 保留之前的数据
        with open(path, mode="w") as fp:
            json.dump(data, fp)
            return len(data)
    return -1

def mark_label(data, label):
    """标记一个数据。

    Args:
        data: 需要被标记的数据。
        label: 需要标记在数据上的标签。
    
    Returns:
        带有标记的数据。
    """
    return [data, label]

def extract_labeled_data(data):
    """解构一个带有标记的数据。

    Args:
        data: 带有标记的数据。
    
    Returns:
        原始数据，数据上的标记。
    """
    return data[0], data[1]

def get_batch(labeled_data_list, size):
    """从有标记数据的列表中抽取指定数量并返回。

    Args:
        labeled_data_list: 保存被标记过的数据的列表。
        size: 抽取的数量。
    
    Returns:
        原始数据列表，数据的标记列表。
    """
    samples = random.sample(labeled_data_list, k=size)
    data = []
    labels = []

    for s in samples:
        value, label = extract_labeled_data(s)
        data.append(value)
        labels.append(label)
    return data, labels