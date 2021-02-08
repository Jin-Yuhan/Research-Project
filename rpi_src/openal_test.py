'''
author: Jin Yuhan
date: 2021-02-08 18:47:00
lastTime: 2021-02-08 23:10:07
'''

from openal.audio_listener import AudioListener
from openal.audio_clip import *
from openal.audio_source import *
import time
import math

#load listener
listener = AudioListener((0, 0, 0))
#initialize sound
sound = AudioClip('tone5.wav')
#load sound player
source = AudioSource()

#listener.position = 
source.position = (0, 0, 0)

#load sound into player
source.add(sound)
#enable loop sound so it plays forever
source.loop = True
#set rolloff factor
source.rolloff = 0.01
#play sound
source.play()

a = 30
b = 20
for theta in range(0, 360, 18):
    r = math.radians(theta)
    source.position = (a * math.cos(r) + 10, 0, b * math.sin(r) + 5)
    time.sleep(1)

#stop player
source.stop()