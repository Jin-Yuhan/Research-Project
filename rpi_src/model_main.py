# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-09 17:33:18
lastTime: 2021-02-13 21:43:12
'''

import configs
import tfmodels
from openal import *
from time import sleep
from datetime import datetime
from async_receiver import AsyncHumanDataReceiver

def handle_error(e):
    pass # 记录下错误，再让树莓派闪灯之类的...

def temp(a, b, t):
    return a + t * (b - a)

def slerp(a, b, t):
    x1, y1, z1 = map(float, a)
    x2, y2, z2 = map(float, b)
    return [temp(x1, x2, t), temp(y1, y2, t), temp(z1, z2, t)]

def update(value, pos, delta_time):
    # 最好再给一个置信度
    target_pos = [pos[i] + value[i] for i in range(3)]
    return slerp(pos, target_pos, delta_time)

def main():
    al = OpenAL()  # 必须最先初始化
    listener = AudioListener(**configs.audio_listener)
    source = AudioSource(**configs.audio_source)
    receiver = AsyncHumanDataReceiver(handle_error, **configs.arduino)
    model = tfmodels.RuntimeModel(**configs.tfmodel_common)

    target_delta_time = 1.0 / configs.target_fps
    time = datetime.now()
    
    try:
        source.play()
        receiver.start()

        while receiver.active:
            last_time = time
            time = datetime.now()
            delta_time = (time - last_time).total_seconds()
            
            value = model.run([receiver.latest_data])
            source.position = update(value, source.position, delta_time)  # 更新

            sleep_time = target_delta_time - delta_time
            if sleep_time > 0.1:
                sleep(sleep_time)  # update执行时间太短，等待一波
                print("Sleep:", sleep_time)
    except Exception as e:
        handle_error(e)
    finally:
        source.stop()
        receiver.stop()
        model.close()
        del al, listener, source

if __name__ == "__main__":
    main()
