# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 22:35:00
lastTime: 2021-02-16 16:07:15
'''

from openal.al import *

class AudioListener(object):
    def __init__(self, **kwargs):
        self.position = kwargs.get("position", [0, 0, 0])
        self.orientation = kwargs.get("orientation", [0, 0, 1, 0, 1, 0])

    def destroy(self):
        print("Destroy audio listener.")

    @property
    def position(self) -> list:
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        x, y, z = map(float, value)
        alListener3f(AL_POSITION, x, y, z)

    @property
    def orientation(self) -> list:
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        alListenerfv(AL_ORIENTATION, (ALfloat * 6)(*value))
