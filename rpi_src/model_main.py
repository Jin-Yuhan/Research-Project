# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-09 17:33:18
lastTime: 2021-02-16 17:50:57
'''

import configs
import tfmodels
import numpy as np
from openal import *
from time import sleep
from datetime import datetime
from async_receiver import AsyncDataReceiver

ZEROS = np.zeros(3)

def handle_error(e):
    print(e)  # 记录下错误，再让树莓派闪灯之类的...

def approximate(a, b):
    delta = np.abs(a - b)
    return np.all(delta < configs.epsilon)

def lerp(a, b, t):
    return a + t * (b - a)  # 线性插值

def slerp(a, b, t):
    # 球面线性插值
    am = np.linalg.norm(a)
    bm = np.linalg.norm(b)
    tm = lerp(am, bm, t)
    
    cosw = np.around(np.dot(a, b) / (am * bm), 4)
    sinw = np.sqrt(1 - cosw * cosw)
    
    if sinw == 0:
        ak = 1 - t
        bk = t
    else:
        w = np.arccos(cosw)
        ak = (tm / am) * (np.sin((1 - t) * w) / sinw)
        bk = (tm / bm) * (np.sin(t * w) / sinw)
    return (ak * a) + (bk * b)

def update(pos, direction, distance, delta_time):
    pos = np.array(pos)
    target = np.array(direction) * distance
    t = delta_time * configs.slerp_speed

    if approximate(pos, ZEROS) or approximate(target, ZEROS):
        pos = lerp(pos, target, t)  # 防止除以0
    else:
        pos = slerp(pos, target, t)

    if approximate(pos, target):
        pos = target
    return pos.tolist()

def main():
    al = OpenAL()  # 必须最先初始化
    listener = AudioListener(**configs.audio_listener)
    source = AudioSource(**configs.audio_source)
    receiver = AsyncDataReceiver(handle_error, **configs.arduino)
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
            data = receiver.latest_data
            
            if data:
                direction, distance = model.run([data])
                source.position = update(
                    source.position,
                    direction,
                    distance,
                    delta_time
                )  # 更新
                print("Position:", source.position)

                if source.position == [0, 0, 0]:
                    source.volume = 0
                elif source.volume != 1:
                    source.volume = 1
            
            sleep_time = target_delta_time - delta_time
            if sleep_time >= configs.min_sleep_seconds:
                sleep(sleep_time)  # update执行时间太短，等待
                print("Sleep:", sleep_time)
    except Exception as e:
        handle_error(e)
    finally:
        model.close()
        receiver.stop()
        source.stop()
        source.destroy()
        listener.destroy()
        al.destroy()

if __name__ == "__main__":
    main()
