# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 17:30:32
lastTime: 2021-02-09 18:35:43
'''

from openal.bindings import native_impl
from ctypes import *

ALboolean = c_char
ALchar = c_char
ALbyte = c_char
ALubyte = c_ubyte
ALshort = c_short
ALushort = c_ushort
ALint = c_int
ALuint = c_uint
ALsizei = c_int
ALenum = c_int
ALfloat = c_float
ALdouble = c_double
ALvoid = None

AL_INVALID = -1
AL_NONE = 0
AL_FALSE = 0
AL_TRUE = 1
AL_SOURCE_RELATIVE = 0x202
AL_CONE_INNER_ANGLE = 0x1001
AL_CONE_OUTER_ANGLE = 0x1002
AL_PITCH = 0x1003
AL_POSITION = 0x1004
AL_DIRECTION = 0x1005
AL_VELOCITY = 0x1006
AL_LOOPING = 0x1007
AL_BUFFER = 0x1009
AL_GAIN = 0x100A
AL_MIN_GAIN = 0x100D
AL_MAX_GAIN = 0x100E
AL_ORIENTATION = 0x100F
AL_CHANNEL_MASK = 0x3000
AL_SOURCE_STATE = 0x1010
AL_INITIAL = 0x1011
AL_PLAYING = 0x1012
AL_PAUSED = 0x1013
AL_STOPPED = 0x1014
AL_BUFFERS_QUEUED = 0x1015
AL_BUFFERS_PROCESSED = 0x1016
AL_SEC_OFFSET = 0x1024
AL_SAMPLE_OFFSET = 0x1025
AL_BYTE_OFFSET = 0x1026
AL_SOURCE_TYPE = 0x1027
AL_STATIC = 0x1028
AL_STREAMING = 0x1029
AL_UNDETERMINED = 0x1030
AL_FORMAT_MONO8 = 0x1100
AL_FORMAT_MONO16 = 0x1101
AL_FORMAT_STEREO8 = 0x1102
AL_FORMAT_STEREO16 = 0x1103
AL_REFERENCE_DISTANCE = 0x1020
AL_ROLLOFF_FACTOR = 0x1021
AL_CONE_OUTER_GAIN = 0x1022
AL_MAX_DISTANCE = 0x1023
AL_FREQUENCY = 0x2001
AL_BITS = 0x2002
AL_CHANNELS = 0x2003
AL_SIZE = 0x2004
AL_UNUSED = 0x2010
AL_PENDING = 0x2011
AL_PROCESSED = 0x2012
AL_NO_ERROR = AL_FALSE
AL_INVALID_NAME = 0xA001
AL_ILLEGAL_ENUM = 0xA002
AL_INVALID_ENUM = 0xA002
AL_INVALID_VALUE = 0xA003
AL_ILLEGAL_COMMAND = 0xA004
AL_INVALID_OPERATION = 0xA004
AL_OUT_OF_MEMORY = 0xA005
AL_VENDOR = 0xB001
AL_VERSION = 0xB002
AL_RENDERER = 0xB003
AL_EXTENSIONS = 0xB004
AL_DOPPLER_FACTOR = 0xC000
AL_DOPPLER_VELOCITY = 0xC001
AL_SPEED_OF_SOUND = 0xC003
AL_DISTANCE_MODEL = 0xD000
AL_INVERSE_DISTANCE = 0xD001
AL_INVERSE_DISTANCE_CLAMPED = 0xD002
AL_LINEAR_DISTANCE = 0xD003
AL_LINEAR_DISTANCE_CLAMPED = 0xD004
AL_EXPONENT_DISTANCE = 0xD005
AL_EXPONENT_DISTANCE_CLAMPED = 0xD006

# ------------------------------------------------------------------
# Function Bindings
# ------------------------------------------------------------------

@native_impl(returns=ALenum)
def alGetError():
    pass

# ------------------------------------------------------------------
# Buffer Functions
# ------------------------------------------------------------------

@native_impl(ALsizei, POINTER(ALuint), get_error=alGetError)
def alGenBuffers(n, buffers):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The buffer array isn't large enough to hold the number of buffers requested.",
        AL_OUT_OF_MEMORY: "There is not enough memory available to generate all the buffers requested."
    }

@native_impl(ALsizei, POINTER(ALuint), get_error=alGetError)
def alDeleteBuffers(n, buffers):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_OPERATION: "The buffer is still in use and can not be deleted.",
        AL_INVALID_NAME: "A buffer name is invalid.",
        AL_INVALID_VALUE: "The requested number of buffers can not be deleted."
    }

@native_impl(ALuint, ALenum, POINTER(ALvoid), ALsizei, ALsizei, get_error=alGetError)
def alBufferData(buffer, format, data, size, freq):
    return {
        AL_NO_ERROR: None,
        AL_OUT_OF_MEMORY: "There is not enough memory available to create this buffer.",
        AL_INVALID_VALUE: "The size parameter is not valid for the format specified, the buffer is in use, or the data is a NULL pointer.",
        AL_INVALID_ENUM: "The specified format does not exist.",
    }

# ------------------------------------------------------------------
# Source Functions
# ------------------------------------------------------------------

@native_impl(ALsizei, POINTER(ALuint), get_error=alGetError)
def alGenSources(n, sources):
    return {
        AL_NO_ERROR: None,
        AL_OUT_OF_MEMORY: "There is not enough memory to generate all the requested sources.",
        AL_INVALID_VALUE: "There are not enough non-memory resources to create all the requested sources, or the array pointer is not valid.",
        AL_INVALID_OPERATION: "There is no context to create sources in."
    }

@native_impl(ALsizei, POINTER(ALuint), get_error=alGetError)
def alDeleteSources(n, sources):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_NAME: "At least one specified source is not valid, or an attempt is being made to delete more sources than exist. ",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, get_error=alGetError)
def alIsSource(source):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, ALfloat, get_error=alGetError)
def alSourcef(source, param, value):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is out of range.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, ALfloat, ALfloat, ALfloat, get_error=alGetError)
def alSource3f(source, param, v1, v2, v3):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is out of range.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, POINTER(ALfloat), get_error=alGetError)
def alSourcefv(source, param, values):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is out of range.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, ALint, get_error=alGetError)
def alSourcei(source, param, value):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is out of range.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, ALint, ALint, ALint, get_error=alGetError)
def alSource3i(source, param, v1, v2, v3):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is out of range.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, POINTER(ALint), get_error=alGetError)
def alSourceiv(source, param, values):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is out of range.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, POINTER(ALfloat), get_error=alGetError)
def alGetSourcef(source, pname, value):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, POINTER(ALfloat), POINTER(ALfloat), POINTER(ALfloat), get_error=alGetError)
def alGetSource3f(source, pname, v1, v2 ,v3):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, POINTER(ALfloat), get_error=alGetError)
def alGetSourcefv(source, pname, values):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, POINTER(ALint), get_error=alGetError)
def alGetSourcei(source, pname, value):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, POINTER(ALint), POINTER(ALint), POINTER(ALint), get_error=alGetError)
def alGetSource3i(source, pname, v1, v2 ,v3):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALenum, POINTER(ALint), get_error=alGetError)
def alGetSourceiv(source, pname, values):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, get_error=alGetError)
def alSourcePlay(source):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, get_error=alGetError)
def alSourcePause(source):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, get_error=alGetError)
def alSourceStop(source):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, get_error=alGetError)
def alSourceRewind(source):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALuint, ALsizei, POINTER(ALuint), get_error=alGetError)
def alSourceQueueBuffers(source, n, buffers):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_NAME: "At least one specified buffer name is not valid, or the specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context, an attempt was made to add a new buffer which is not the same format as the buffers already in the queue, or the source already has a static buffer attached."
    }

@native_impl(ALuint, ALsizei, POINTER(ALuint), get_error=alGetError)
def alSourceUnqueueBuffers(source, n, buffers):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "At least one buffer can not be unqueued because it has not been processed yet.",
        AL_INVALID_NAME: "The specified source name is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

# ------------------------------------------------------------------
# Listener Functions
# ------------------------------------------------------------------

@native_impl(ALenum, ALfloat, get_error=alGetError)
def alListenerf(param, value):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, ALfloat, ALfloat, ALfloat, get_error=alGetError)
def alListener3f(param, v1, v2, v3):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, POINTER(ALfloat), get_error=alGetError)
def alListenerfv(param, values):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, ALint, get_error=alGetError)
def alListeneri(param, value):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, ALint, ALint, ALint, get_error=alGetError)
def alListener3i(param, v1, v2, v3):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, POINTER(ALint), get_error=alGetError)
def alListeneriv(param, values):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, POINTER(ALfloat), get_error=alGetError)
def alGetListenerf(param, value):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, POINTER(ALfloat), POINTER(ALfloat), POINTER(ALfloat), get_error=alGetError)
def alGetListener3f(param, v1, v2, v3):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, POINTER(ALfloat), get_error=alGetError)
def alGetListenerfv(param, values):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, POINTER(ALint), get_error=alGetError)
def alGetListeneri(param, value):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, POINTER(ALint), POINTER(ALint), POINTER(ALint), get_error=alGetError)
def alGetListener3i(param, v1, v2, v3):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }

@native_impl(ALenum, POINTER(ALint), get_error=alGetError)
def alGetListeneriv(param, values):
    return {
        AL_NO_ERROR: None,
        AL_INVALID_VALUE: "The value pointer given is not valid.",
        AL_INVALID_ENUM: "The specified parameter is not valid.",
        AL_INVALID_OPERATION: "There is no current context."
    }
