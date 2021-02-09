# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 18:47:00
lastTime: 2021-02-09 23:09:43
'''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import math
import time
from openal import *

listener = AudioListener()  # 必须最先初始化
listener.orientation = (0, 0, 1, 0, 1, 0)
listener.position = (0, 0, 0)

source = AudioSource()
source.clip = AudioClip.create_from_file("tone5.wav")
source.loop = True
source.rolloff = 0.01
source.direction = (0, 0, 1)
source.position = (0, 0, 0)
source.play()

a = 30
b = 20

for theta in range(0, 360, 18):
    r = math.radians(theta)
    pos = (a * math.cos(r), 0, b * math.sin(r))
    source.position = pos
    print(pos)
    time.sleep(1)

source.stop()
