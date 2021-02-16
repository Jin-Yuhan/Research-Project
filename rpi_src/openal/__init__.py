# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 17:28:09
lastTime: 2021-02-16 14:53:02
'''

class OpenAL(object):
    def __init__(self):
        import openal.alc as alc
        self.device = alc.alcOpenDevice(None)  # select the "preferred device"

        if not self.device:
            print("Open device failed!")
            return
        
        self.context = alc.alcCreateContext(self.device, None)
        if not self.context:
            print("Create context failed!")
        elif not alc.alcMakeContextCurrent(self.context):
            print("Make context current failed!")
        else:
            print("Initialize OpenAL.")

    def destroy(self):
        import openal.alc as alc
        alc.alcMakeContextCurrent(None)
        
        if self.context:
            alc.alcDestroyContext(self.context)
            
        if self.device:
            alc.alcCloseDevice(self.device)
        
        print("Destroy OpenAL.")

from openal.audio_clip import AudioClip
from openal.audio_listener import AudioListener
from openal.audio_source import AudioSource
