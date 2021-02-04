'''
author: Jin Yuhan
date: 2021-01-25 18:06:29
lastTime: 2021-02-03 20:44:20
'''

def print_arduino_data(data):
    print("Arduino Data:")
    print("\tAcceleration:", data[0:3])
    print("\tAngular Velocity:", data[3:6])
    print("\tRotation:", data[6:9])
    print("\tLeft Pressures:", data[9:12])
    print("\tRight Pressures:", data[12:15])
