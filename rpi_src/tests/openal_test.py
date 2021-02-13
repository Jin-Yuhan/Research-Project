# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 18:47:00
lastTime: 2021-02-13 20:28:20
'''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import math
import time
import configs
from openal import *

al = OpenAL()  # 必须最先初始化
source = AudioSource(**configs.audio_source)
listener = AudioListener(**configs.audio_listener)
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
del source, listener, al