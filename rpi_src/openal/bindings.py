# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-09 18:34:47
lastTime: 2021-02-16 15:00:38
'''

from ctypes import CDLL
from functools import wraps

dll = CDLL("openal32")
print("Load openal32 dll:", dll)

def native_impl(*argtypes, returns=None, name=None):
    """指示函数在 openal 库中实现。

    被装饰的函数在被调用时，首先会调用 openal32 库中
    具有指定名称的函数，之后被装饰函数的函数体才会被执行。

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
        print("Load native function: {}.".format(native_name))
        
        @wraps(func)
        def func_wrap(*args, **kwargs):
            value = native_func(*args, **kwargs)
            func(*args, **kwargs)  # 回调
            return value
        return func_wrap
    return native_decorator
