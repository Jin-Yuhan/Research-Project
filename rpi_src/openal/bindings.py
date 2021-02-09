# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-09 18:34:47
lastTime: 2021-02-09 18:34:47
'''

from ctypes import CDLL
from functools import wraps

dll = CDLL("openal32.dll")

class OpenALError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)

def native_impl(*argtypes, returns=None, name=None, get_error=None):
    """指示函数在 openal 库中实现。

    Args:
        argtypes: 参数类型列表。
        returns: 返回值类型。如果该值为None，则没有返回值(void)。
        name: 函数在类库中的名称。如果该值为None，则使用定义的函数的名称。
        get_error: 用于获取错误码的函数。

    Raises:
        TypeError: 函数返回值类型错误。
        ValueError: 获取错误码的函数无法被调用。

    Remarks:
        如果设置了获取错误码的函数，那么被装饰的函数的返回值必须是一个字典，
        其键为错误码，值为错误消息。如果错误消息为None，那么这个错误码不会导致一个异常的抛出。
    """
    def native_decorator(func):
        native_name = name if name else func.__name__
        native_func = getattr(dll, native_name)
        native_func.argtypes = argtypes
        native_func.restype = returns
        error_map = None  # 异常与异常消息的映射

        if callable(get_error):
            error_map = func(*argtypes)  # 在保证数量的前提下任意传入参数
            if not isinstance(error_map, dict):
                raise TypeError("The type of the return value must be 'dict'!")
        elif get_error is not None:  # 如果为None，就不管了
            raise ValueError("The parameter 'get_error' must be callable!")

        print("Load native function: {}.".format(native_name))

        @wraps(func)
        def func_wrap(*args, **kwargs):
            value = native_func(*args, **kwargs)
            if error_map:
                error = get_error()
                if error in error_map:
                    msg = error_map[error]
                    if msg: raise OpenALError(msg)  # 如果msg为None，则没有异常
                else:
                    raise OpenALError("Unhandled Error Code: {}.".format(error))
            return value
        return func_wrap
    return native_decorator