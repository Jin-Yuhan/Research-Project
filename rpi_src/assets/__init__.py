# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-13 17:17:57
lastTime: 2021-02-13 17:50:19
'''

import os

def get_absolute_path(relative_path) -> str:
    """获取资源的绝对路径。

    Args:
        relative_path (str): 资源在assets目录下的相对路径。
        
    Returns:
        str: 资源的绝对路径。
    """
    directory = os.path.dirname(__file__)
    return os.path.join(directory, relative_path)
