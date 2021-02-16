# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-27 17:42:49
lastTime: 2021-02-16 15:38:44
'''

from arduino_api import ArduinoDataReceiver
from threading import Thread

class AsyncDataReceiver(object):
    """表示异步的数据接收器。

    Attributes:
        error_handler: 接收数据遇到错误时调用的回调函数，参数为错误对象。
    """
    def __init__(self, error_handler, **kwargs):
        """初始化 AsyncDataReceiver 实例。

        初始化一个具有指定参数的 AsyncDataReceiver 实例。

        Args:
            error_handler: 接收数据遇到错误时调用的回掉函数，参数为错误对象。
            kwargs: 可选的键值对参数。可选值同 ArduinoDataReceiver。
        """
        self.error_handler = error_handler
        self._configs = kwargs
        self._reset()

    def _reset(self):
        self._active = False
        self._thread = None
        self._raw_data = None

    def _receive_data_async(self):
        with ArduinoDataReceiver(**self._configs) as receiver:
            while self._active:
                try:
                    self._raw_data = receiver.receive()
                except Exception as e:
                    if self.error_handler:
                        self.error_handler(e)
                    else:
                        raise  # 错误没有被处理，重新抛出

    @property
    def active(self):
        """获取是否正在接收数据。"""
        return self._active and self._thread and self._thread.is_alive()

    @property
    def latest_raw_data(self):
        """获取最新的原始数据（15维向量）。"""
        return self._raw_data if self.active else None

    @property
    def latest_data(self):
        """获取最新的处理后的数据（14维向量）。"""
        data = self.latest_raw_data
        return [
            # 姿态数据
            *data[0:9],

            # 左右平衡差值
            data[9] - data[12],
            data[10] - data[13],
            data[11] - data[14],

            # 前后平衡差值
            ((data[9] + data[10]) * 0.5) - data[11],
            ((data[12] + data[13]) * 0.5) - data[14]
        ] if data else None

    def start(self):
        """开始接收数据。"""
        if not self.active:
            self._reset()
            self._active = True
            self._thread = Thread(target=self._receive_data_async)
            self._thread.start()

    def stop(self):
        """停止接收数据。"""
        if self.active:
            self._active = False
            self._thread.join()
