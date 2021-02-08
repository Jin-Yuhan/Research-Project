# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 17:28:09
lastTime: 2021-02-08 22:52:10
'''

from ctypes import CDLL
from functools import wraps

dll = CDLL("openal32.dll")

def native_impl(*argtypes, returns=None, name=None):
    """指示函数的实现在 openal 库中。

    Args:
        argtypes: 参数类型列表。
        returns: 返回值类型。如果该值为None，则没有返回值(void)。
        name: 函数在类库中的名称。如果该值为None，则使用定义的函数的名称。
    """
    def native_decorator(func):
        native_name = name if name else func.__name__
        native_func = getattr(dll, native_name)
        native_func.argtypes = argtypes
        native_func.restype = returns
        print("load native function: {}.".format(native_name))
        @wraps(func)
        def func_wrap(*args, **kwargs):
            return native_func(*args, **kwargs)
        return func_wrap
    return native_decorator

class OpenALError(RuntimeError):
    def __init__(self, *args):
        super(RuntimeError, self).__init__(*args)