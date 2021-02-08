# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 22:35:00
lastTime: 2021-02-08 23:09:50
'''
from openal import OpenALError
from openal.al import *
from openal.alc import *
import ctypes

class AudioListener(object):
    def __init__(self):
        self._device = alcOpenDevice(None)  # select the "preferred device"

        if self._device:
            self._context = alcCreateContext(self._device, None)
            alcMakeContextCurrent(self._context)
        
        self.check_error()

    def __del__(self):
        if self._context:
            alcDestroyContext(self._context)
        if self._device:
            alcCloseDevice(self._device)

    def check_error(self):
        error = alGetError()
        if error != AL_NO_ERROR:
            raise OpenALError("AudioListener Error Code: {}".format(error))

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        x, y, z = map(int, value)
        alListener3f(AL_POSITION, x, y, z)
        self.check_error()

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        # ...
        self.check_error()