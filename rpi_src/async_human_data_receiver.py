# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-27 17:42:49
lastTime: 2021-02-09 18:37:42
'''

from arduino_api import ArduinoDataReceiver
from threading import Thread

class AsyncHumanDataReceiver(object):
    """表示异步的人体数据的接收器。

    Attributes:
        error_handler: 接收数据遇到错误时调用的回掉函数，参数为错误对象。
    """
    def __init__(self, error_handler, **kwargs):
        """初始化 AsyncHumanDataReceiver 实例。

        初始化一个具有指定参数的 AsyncHumanDataReceiver 实例。

        Args:
            error_handler: 接收数据遇到错误时调用的回掉函数，参数为错误对象。
            kwargs: 可选的键值对参数。可选值同 ArduinoDataReceiver。
        """
        self.error_handler = error_handler
        self.__configs = kwargs
        self.__reset()

    def __reset(self):
        self.__active = False
        self.__thread = None
        self.__data = None

    def __receive_data_async(self):
        with ArduinoDataReceiver(**self.__configs) as receiver:
            while self.__active:
                try:
                    self.__data = receiver.receive()
                except Exception as e:
                    if self.error_handler:
                        self.error_handler(e)
                    else:
                        raise  # 错误没有被处理，重新抛出

    @property
    def active(self):
        """获取是否正在接收数据。"""
        return self.__active and self.__thread and self.__thread.is_alive()

    @property
    def latest_data(self):
        """获取最新的数据。"""
        return self.__data if self.active else None

    def start(self):
        """开始接收数据。"""
        if not self.active:
            self.__reset()
            self.__active = True
            self.__thread = Thread(target=self.__receive_data_async)
            self.__thread.start()

    def stop(self):
        """停止接收数据。"""
        if self.active:
            self.__active = False
            self.__thread.join()
