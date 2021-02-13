# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 17:28:20
lastTime: 2021-02-13 19:18:20
'''

from openal.al import *
from openal.audio_clip import load_from_file

class AudioSource(object):
    def __init__(self, **kwargs):
        self._source = ALuint(0)
        alGenSources(1, self._source)
        
        self.clip = load_from_file(kwargs.get("clip", None))
        self.source_relative = kwargs.get("source_relative", False)
        self.position = kwargs.get("position", [0, 0, 0])
        self.direction = kwargs.get("direction", [0, 0, 1])
        self.rolloff = kwargs.get("rolloff", 0)
        self.loop = kwargs.get("loop", False)
        self.pitch = kwargs.get("pitch", 1.0)
        self.volume = kwargs.get("volume", 1.0)

    def __del__(self):
        alDeleteSources(1, self._source)

    @property
    def clip(self):
        return self._clip

    @clip.setter
    def clip(self, value):
        self._clip = value
        buffer = ALint(value.buffer.value) if value else 0
        alSourcei(self._source, AL_BUFFER, buffer)

    @property
    def source_relative(self):
        return self._source_relative

    @source_relative.setter
    def source_relative(self, value):
        self._source_relative = value
        alSourcei(self._source, AL_SOURCE_RELATIVE, value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        x, y, z = map(float, value)
        alSource3f(self._source, AL_POSITION, x, y, z)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value
        x, y, z = map(float, value)
        alSource3f(self._source, AL_DIRECTION, x, y, z)

    @property
    def rolloff(self):
        return self._rolloff

    @rolloff.setter
    def rolloff(self, value):
        self._rolloff = value
        alSourcef(self._source, AL_ROLLOFF_FACTOR, value)

    @property
    def loop(self):
        return self._loop
    
    @loop.setter
    def loop(self, value):
        self._loop = value
        alSourcei(self._source, AL_LOOPING, value)

    @property
    def pitch(self):
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        self._pitch = value
        alSourcef(self._source, AL_PITCH, value)

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        alSourcef(self._source, AL_GAIN, value)

    @property
    def is_playing(self):
        state = ALint(0)
        alGetSourcei(self._source, AL_SOURCE_STATE, state)
        return state.value == AL_PLAYING

    def play(self):
        alSourcePlay(self._source)

    def stop(self):
        alSourceStop(self._source)

    def rewind(self):
        alSourceRewind(self._source)

    def pause(self):
        alSourcePause(self._source)
