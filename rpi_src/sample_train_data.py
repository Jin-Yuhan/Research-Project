# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-01-25 20:01:49
lastTime: 2021-02-09 18:40:56
'''

from async_human_data_receiver import AsyncHumanDataReceiver
import train_data as td
import configs

def main():
    sample_list = []
    receiver = AsyncHumanDataReceiver(None, **configs.arduino)
    receiver.start()
    
    while receiver.active:
        try:
            value = int(input(">>> "))
        except ValueError:
            print("The input value must be an integer.")
            continue

        if value > 0 and value < 9:
            data = receiver.latest_data
            if data:
                label = [int(i == value) for i in range(1, 9)]
                sample_list.append(td.mark_label(data, label))
                print(sample_list[-1])
        elif value == -1:
            break
        else:
            print("The input value must be in [1,9), or equal -1.")
    
    receiver.stop()
    saved_count = td.save_to_path(configs.TRAIN_DATA_SAVE_PATH, sample_list)

    if saved_count > 0:
        print("%d train data saved!" % saved_count)
    else:
        print("Train data save failed!")

if __name__ == "__main__":
    main()