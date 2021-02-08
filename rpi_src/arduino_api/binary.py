# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-27 11:32:40
lastTime: 2021-02-08 15:25:42
'''

class BinaryReader(object):
    """表示二进制数据的读取器。"""
    def __init__(self, buffer, start_index=0):
        """初始化 BinaryReader 实例。

        初始化一个具有给定缓冲区和起始索引位置的 BinaryReader 实例。

        Args:
            buffer: 缓冲区。
            start_index: 起始索引位置。
            
        Raises:
            ValueError: buffer 为空。
            IndexError: start_index 超出范围。
        """
        if not buffer:
            raise ValueError("The parameter buffer({}) is empty."
                            .format(buffer))

        if start_index < 0 or start_index >= len(buffer):
            raise IndexError("The parameter start_index({}) is out of bounds."
                            .format(start_index))

        self.__buffer = buffer
        self.__index = start_index

    def read_two_bytes_little_endian(self):
        """读取两个字节，并以小字节序返回。

        从缓冲区中读取两个字节，并将索引位置向后移动两个字节，
        最后以小字节序返回这两个字节。

        Returns:
            从缓冲区中读取的两个字节，顺序为：低位字节，高位字节。

        Raises:
            EOFError: 已经读取至缓冲区末端。
        """
        if self.__index > len(self.__buffer) - 2:
            raise EOFError("BinaryReader index: {}, buffer_size: {}."
                            .format(self.__index, len(self.__buffer)))

        low = self.__buffer[self.__index]  # Arduino 端是 Little Endian
        high = self.__buffer[self.__index + 1]
        self.__index += 2
        return low, high

    def read_int(self, signed=True):
        """读取一个整数，并返回。

        从缓冲区中读取一个整数，并将索引位置向后移动，最后返回这个数。

        Args:
            signed: 指示该整数是否为有符号整数。

        Returns:
            从缓冲区中读取这个整数。

        Raises:
            EOFError: 已经读取至缓冲区末端。
        """
        low, high = self.read_two_bytes_little_endian()

        # 因为从 Arduino 发送的整数都由两个字节组成，
        # 而 Python 的 int 类型占用的字节数大于2，所以当整数有符号时，
        # ((high << 8) | low) 运算会将它的符号位当做数值位处理，
        # 导致结果可能出现错误。

        if signed:
            v = ((high & 0x7F) << 8) | low
            return v if (high & 0x80) == 0 else -((~(v - 1)) & 0x7FFF)
        else:
            return (high << 8) | low
        
    def read_float(self):
        """读取一个浮点数，并返回。

        从缓冲区中读取一个浮点数，并将索引位置向后移动，最后返回这个数。

        Returns:
            从缓冲区中读取这个浮点数。

        Raises:
            EOFError: 已经读取至缓冲区末端。
        """
        return self.read_int(signed=True) / 32768.0

    def read_int_many(self, results, count, decorator, signed=True):
        """读取许多整数，并返回。

        从缓冲区中读取指定数量的整数，并将索引位置向后移动，最后将这组数添加到指定列表中。

        Args:
            results: 用于保存结果的列表。
            count: 需要读取的整数个数。
            decorator: 每次读取一个整数都会调用的回调函数，参数为这次读取的整数，
                其返回值将作为本次读取的最终值。
            signed: 指示该整数是否为有符号整数。

        Raises:
            EOFError: 已经读取至缓冲区末端。
        """
        for _ in range(count):
            value = decorator(self.read_int(signed=signed))
            results.append(value)

    def read_float_many(self, results, count, decorator):
        """读取许多浮点数，并返回。

        从缓冲区中读取指定数量的浮点数，并将索引位置向后移动，最后将这组数添加到指定列表中。

        Args:
            results: 用于保存结果的列表。
            count: 需要读取的浮点数个数。
            decorator: 每次读取一个浮点数都会调用的回调函数，参数为这次读取的浮点数，
                其返回值将作为本次读取的最终值。

        Raises:
            EOFError: 已经读取至缓冲区末端。
        """
        for _ in range(count):
            value = decorator(self.read_float())
            results.append(value)