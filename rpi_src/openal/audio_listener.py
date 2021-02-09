# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 22:35:00
lastTime: 2021-02-09 19:33:08
'''

from openal.al import *
from openal.alc import *

class AudioListener(object):
    def __init__(self, **kwargs):
        self._device = alcOpenDevice(None)  # select the "preferred device"

        if self._device:
            self._context = alcCreateContext(self._device, None)
            alcMakeContextCurrent(self._context)
            
            self.position = kwargs.get("position", [0, 0, 0])
            self.orientation = kwargs.get("orientation", [0, 0, 1, 0, 1, 0])

    def __del__(self):
        alcMakeContextCurrent(None)
        alcDestroyContext(self._context)
        alcCloseDevice(self._device)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        x, y, z = map(float, value)
        alListener3f(AL_POSITION, x, y, z)

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        alListenerfv(AL_ORIENTATION, (ALfloat * 6)(*value))
