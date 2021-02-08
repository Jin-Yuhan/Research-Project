# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-27 14:39:23
lastTime: 2021-02-08 15:41:42
'''

from arduino_api.receiver import ArduinoDataReceiver

def print_arduino_data(data, print_func=print):
    print_func("Acceleration: {}".format(data[0:3]))
    print_func("Angular Velocity: {}".format(data[3:6]))
    print_func("Rotation: {}".format(data[6:9]))
    print_func("Left Pressures: {}".format(data[9:12]))
    print_func("Right Pressures: {}".format(data[12:15]))