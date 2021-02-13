# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2020-12-19 15:49:32
lastTime: 2021-02-13 20:30:56
'''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import time
import traceback
import configs
import xlwt
from arduino_api import *
from serial.serialutil import SerialException

class ExcelSaver(object):
    __EXCEL_ITEMS = [
        "加速度 X", "加速度 Y", "加速度 Z",
        "角速度 X", "角速度 Y", "角速度 Z",
        "滚转角（X）", "俯仰角（Y）", "偏航角（Z）",
        "压力 A0", "压力 A1", "压力 A2", "压力 A3", "压力 A4", "压力 A5",
    ]

    def __init__(self, encoding="utf-8", sheet_name="sample_data"):
        self.__line = 0
        self.__workbook = xlwt.Workbook(encoding=encoding)
        self.__worksheet = self.__workbook.add_sheet(sheet_name)
        
        self.write(ExcelSaver.__EXCEL_ITEMS)

    def write(self, data):
        for i in range(len(data)):
            self.__worksheet.write(self.__line, i, data[i])
        self.__line += 1
        
    def save(self, file_name):
        self.__workbook.save(file_name)

if __name__ == '__main__':
    saver = ExcelSaver()
    sample_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    file_name = sample_name + ".xls"
    i = 0

    with ArduinoDataReceiver(**configs.arduino) as receiver:
        while True:
            try:
                data = receiver.receive()
            except SerialException:
                traceback.print_exc()
                break  # 遇到这个错误基本就没救了...
            except:
                traceback.print_exc()
            else:
                print("[%d]" % i, end=" ")
                print_arduino_data(data)
                saver.write(data)
                if i % 50 == 0:
                    saver.save(file_name)
                i += 1
