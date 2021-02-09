# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 17:32:01
lastTime: 2021-02-09 18:35:52
'''

from openal.bindings import native_impl
from ctypes import *

ALCboolean = c_char
ALCchar = c_char
ALCbyte = c_char
ALCubyte = c_ubyte
ALCshort = c_short
ALCushort = c_ushort
ALCint = c_int
ALCuint = c_uint
ALCsizei = c_int
ALCenum = c_int
ALCfloat = c_float
ALCdouble = c_double
ALCvoid = None

class ALCdevice(Structure):
    pass

class ALCcontext(Structure):
    pass

ALC_INVALID = 0
ALC_FALSE = 0
ALC_TRUE = 1

ALC_FREQUENCY = 0x1007
ALC_REFRESH = 0x1008
ALC_SYNC = 0x1009
ALC_MONO_SOURCES = 0x1010
ALC_STEREO_SOURCES = 0x1011
ALC_NO_ERROR = ALC_FALSE
ALC_INVALID_DEVICE = 0xA001
ALC_INVALID_CONTEXT = 0xA002
ALC_INVALID_ENUM = 0xA003
ALC_INVALID_VALUE = 0xA004
ALC_OUT_OF_MEMORY = 0xA005
ALC_DEFAULT_DEVICE_SPECIFIER = 0x1004
ALC_DEVICE_SPECIFIER = 0x1005
ALC_EXTENSIONS = 0x1006
ALC_MAJOR_VERSION = 0x1000
ALC_MINOR_VERSION = 0x1001
ALC_ATTRIBUTES_SIZE = 0x1002
ALC_ALL_ATTRIBUTES = 0x1003
ALC_DEFAULT_ALL_DEVICES_SPECIFIER = 0x1012
ALC_ALL_DEVICES_SPECIFIER = 0x1013
ALC_CAPTURE_DEVICE_SPECIFIER = 0x310
ALC_CAPTURE_DEFAULT_DEVICE_SPECIFIER = 0x311
ALC_CAPTURE_SAMPLES = 0x312

@native_impl(POINTER(ALCchar), returns=POINTER(ALCdevice))
def alcOpenDevice(devicename):
    pass

@native_impl(POINTER(ALCdevice), returns=ALCboolean)
def alcCloseDevice(device):
    pass

@native_impl(POINTER(ALCdevice), POINTER(ALCint), returns=POINTER(ALCcontext))
def alcCreateContext(device, attrlist):
    pass

@native_impl(POINTER(ALCcontext), returns=ALCboolean)
def alcMakeContextCurrent(context):
    pass

@native_impl(POINTER(ALCcontext))
def alcDestroyContext(context):
    pass
