# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 17:28:20
lastTime: 2021-02-08 23:24:51
'''
from openal import al, alc

class AudioSource(object):
    def __init__(self, **kwargs):
        self.__source = al.ALuint(0)
        al.alGenSources(1, self.__source)
    #disable rolloff factor by default
        al.alSourcef(self.__source, al.AL_ROLLOFF_FACTOR, 0)
    #disable source relative by default
        al.alSourcei(self.__source, al.AL_SOURCE_RELATIVE, 0)
        al.alSourcef(self.__source, al.AL_ORIENTATION, 1)
    #capture player state buffer
        self.state = al.ALint(0)
    #set internal variable tracking
        self.volume = 1.0
        self.pitch = 1.0
        self.position = [0,0,0]
        self.rolloff = 1.0
        self.loop = False
        self.queue = []

    def __del__(self):
        al.alDeleteSources(1, self.__source)

    @property
    def rolloff(self):
        """Get rolloff factor, determines volume based on distance from listener."""
        return self.__rolloff

    @rolloff.setter
    def rolloff(self, value):
        """Set rolloff factor, determines volume based on distance from listener."""
        self.__rolloff = value
        al.alSourcef(self.__source, al.AL_ROLLOFF_FACTOR, al.ALfloat(value))

    @property
    def loop(self):
        """Get whether looping or not."""
        return self.__loop
    
    @loop.setter
    def loop(self, value):
        """Get whether looping or not."""
        self.__loop = value
        al.alSourcei(self.__source, al.AL_LOOPING, value)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        x, y, z = map(al.ALfloat, value)
        al.alSource3f(self.__source, al.AL_POSITION, x, y, z)

    @property
    def pitch(self):
        """Get pitch - 1.5-0.5 float range only."""
        return self.__pitch

    @pitch.setter
    def pitch(self, value):
        """Set pitch - 1.5-0.5 float range only."""
        self.__pitch = value
        al.alSourcef(self.__source, al.AL_PITCH, al.ALfloat(value))

    @property
    def volume(self):
        """Get volume - 1.0 float range only."""
        return self.__volume

    @volume.setter
    def volume(self, value):
        """Set volume - 1.0 float range only."""
        self.__volume = value
        al.alSourcef(self.__source, al.AL_GAIN, al.ALfloat(value))

    @property
    def seek(self):#returns float 0.0-1.0
        """Get current buffer length position (IE: 21000), so divide by the buffers self.length."""
        al.alGetSourcei(self.__source, al.AL_BYTE_OFFSET, self.state)
        return float(self.state.value) / float(self.queue[0].length)

#Go straight to a set point in the sound file
    @seek.setter
    def seek(self,offset):#float 0.0-1.0
        """"""
        al.alSourcei(self.__source, al.AL_BYTE_OFFSET, int(self.queue[0].length * offset))

    @property
    def is_playing(self):
        al.alGetSourcei(self.__source, al.AL_SOURCE_STATE, self.state)
        return self.state.value == al.AL_PLAYING

#queue a sound buffer
    def add(self, sound):
        al.alSourceQueueBuffers(self.__source, 1, sound.buffer) #self.buf
        self.queue.append(sound)

#remove a sound from the queue (detach & unqueue to properly remove)
    def remove(self):
        if len(self.queue) > 0:
            al.alSourceUnqueueBuffers(self.__source, 1, self.queue[0].buffer) #self.buf
            al.alSourcei(self.__source, al.AL_BUFFER, 0)
            self.queue.pop(0)

    def play(self):
        al.alSourcePlay(self.__source)

#stop playing sound
    def stop(self):
        al.alSourceStop(self.__source)

#rewind player
    def rewind(self):
        al.alSourceRewind(self.__source)

#pause player
    def pause(self):
        al.alSourcePause(self.__source)

