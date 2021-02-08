# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 17:28:48
lastTime: 2021-02-08 23:24:25
'''
from openal.al import *
import wave

class AudioClip(object):
    def __init__(self, format, data, size, freq):
        self.buffer = ALuint(0)

        alGenBuffers(1, self.buffer)
        alBufferData(self.buffer, format, data, size, freq)

        print("load audio clip.")

    def __del__(self):
        if self.buffer:
            alDeleteBuffers(1, self.buffer)

class WaveAudioClip(AudioClip):
    FORMAT_MAP = {
        (1, 8): AL_FORMAT_MONO8,
        (2, 8): AL_FORMAT_STEREO8,
        (1, 16): AL_FORMAT_MONO16,
        (2, 16): AL_FORMAT_STEREO16,
    }

    def __init__(self, path):
        wavefp = wave.open(path)
        channels = wavefp.getnchannels()
        bitrate = wavefp.getsampwidth() * 8
        samplerate = wavefp.getframerate()
        wavbuf = wavefp.readframes(wavefp.getnframes())
        alformat = WaveAudioClip.FORMAT_MAP[(channels, bitrate)]
        super(AudioClip, self).__init__(alformat, wavbuf, len(wavbuf), samplerate)
    