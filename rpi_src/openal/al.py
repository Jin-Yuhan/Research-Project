# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 17:30:32
lastTime: 2021-02-08 23:05:22
'''
from openal import native_impl
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

@native_impl(ALenum, ALfloat, ALfloat, ALfloat)
def alListener3f(param, v1, v2, v3):
    """This function sets a floating point property for the listener.

    Args:
        param: the name of the attribute to set: 
            AL_POSITION
            AL_VELOCITY.
        v1, v2, v3: the value to set the attribute to.
    """
    pass

@native_impl(ALenum, POINTER(ALfloat))
def alListenerfv(param, values):
    """This function sets a floating point-vector property of the listener.

    Args:
        param: the name of the attribute to be set:
            AL_POSITION
            AL_VELOCITY
            AL_ORIENTATION.
        values: pointer to floating point-vector values.
    """
    pass

@native_impl(ALsizei, POINTER(ALuint))
def alGenSources(n, sources):
    """This function generates one or more sources. References to sources are ALuint values,
        which are used wherever a source reference is needed (in calls such as alDeleteSources
        and alSourcei). 

    Args:
        n: the number of sources to be generated.
        sources: pointer to an array of ALuint values which will store the names of
            the new sources.
    """
    pass

@native_impl(ALsizei, POINTER(ALuint))
def alDeleteSources(n, sources):
    """This function deletes one or more sources.

    Args:
        n: the number of sources to be deleted.
        sources: pointer to an array of source names identifying the sources to be deleted.
    """
    pass

@native_impl(ALuint, ALenum, ALfloat)
def alSourcef(source, param, value):
    """This function sets a floating point property of a source.

    Args:
        source: source name whose attribute is being set.
        param: the name of the attribute to set:
            AL_PITCH
            AL_GAIN
            AL_MIN_GAIN
            AL_MAX_GAIN
            AL_MAX_DISTANCE
            AL_ROLLOFF_FACTOR
            AL_CONE_OUTER_GAIN
            AL_CONE_INNER_ANGLE
            AL_CONE_OUTER_ANGLE
            AL_REFERENCE_DISTANCE.
        value: the value to set the attribute to.
    """
    pass

@native_impl(ALuint, ALenum, ALfloat, ALfloat, ALfloat)
def alSource3f(source, param, v1, v2, v3):
    """This function sets a source property requiring three floating point values.

    Args:
        source: source name whose attribute is being set.
        param: the name of the attribute to set:
            AL_POSITION
            AL_VELOCITY
            AL_DIRECTION.
        v1, v2, v3: the three ALfloat values which the attribute will be set to.
    """
    pass

@native_impl(ALuint, ALenum, ALint)
def alSourcei(source, param, value):
    """This function sets an integer property of a source.

    Args:
        source: source name whose attribute is being set.
        param: the name of the attribute to set:
            AL_SOURCE_RELATIVE
            AL_CONE_INNER_ANGLE
            AL_CONE_OUTER_ANGLE
            AL_LOOPING
            AL_BUFFER
            AL_SOURCE_STATE.
        value: the value to set the attribute to.
    """
    pass

@native_impl(ALuint, ALenum, ALint, ALint, ALint)
def alSource3i(source, param, v1, v2, v3):
    """This function sets an integer property of a source.

    Args:
        source: source name whose attribute is being set.
        param: the name of the attribute to set:
            AL_POSITION
            AL_VELOCITY
            AL_DIRECTION.
        v1, v2, v3: the values to set the attribute to.
    """
    pass

@native_impl(ALuint, ALenum, POINTER(ALint))
def alGetSourcei(source, pname, value):
    """This function retrieves an integer property of a source.

    Args:
        source: source name whose attribute is being retrieved.
        pname: the name of the attribute to retrieve:
            AL_SOURCE_RELATIVE
            AL_BUFFER
            AL_SOURCE_STATE
            AL_BUFFERS_QUEUED
            AL_BUFFERS_PROCESSED.
        value: a pointer to the integer value being retrieved.
    """
    pass

@native_impl(ALuint)
def alSourcePlay(source):
    """This function plays a source.

    Args:
        source: the name of the source to be played.
    """
    pass

@native_impl(ALuint)
def alSourcePause(source):
    """This function pauses a source. 

    Args:
        source: the name of the source to be paused.
    """
    pass

@native_impl(ALuint)
def alSourceStop(source):
    """This function stops a source.

    Args:
        source: the name of the source to be stopped.
    """
    pass

@native_impl(ALuint)
def alSourceRewind(source):
    """This function stops the source and sets its state to AL_INITIAL.

    Args:
        source: the name of the source to be rewound.
    """
    pass

@native_impl(ALuint, ALsizei, POINTER(ALuint))
def alSourceQueueBuffers(source, n, buffers):
    """This function queues a set of buffers on a source. All buffers attached to a source will be
        played in sequence, and the number of processed buffers can be detected using an
        alSourcei call to retrieve AL_BUFFERS_PROCESSED.

    Args:
        source: the name of the source to queue buffers onto.
        n: the number of buffers to be queued.
        buffers: a pointer to an array of buffer names to be queued.
    """
    pass

@native_impl(ALuint, ALsizei, POINTER(ALuint))
def alSourceUnqueueBuffers(source, n, buffers):
    """This function unqueues a set of buffers attached to a source. The number of processed
        buffers can be detected using an alSourcei call to retrieve AL_BUFFERS_PROCESSED,
        which is the maximum number of buffers that can be unqueued using this call.

    Args:
        source: the name of the source to unqueue buffers from.
        n: the number of buffers to be unqueued.
        buffers: a pointer to an array of buffer names that were removed.
    """
    pass

@native_impl(ALsizei, POINTER(ALuint))
def alGenBuffers(n, buffers):
    """This function generates one or more buffers, which contain audio data (see
        alBufferData). References to buffers are ALuint values, which are used wherever a
        buffer reference is needed (in calls such as alDeleteBuffers, alSourcei,
        alSourceQueueBuffers, and alSourceUnqueueBuffers). 

    Args:
        n: the number of buffers to be generated.
        buffers: pointer to an array of ALuint values which will store the names of
            the new buffers.
    """
    pass

@native_impl(ALsizei, POINTER(ALuint))
def alDeleteBuffers(n, buffers):
    """This function deletes one or more buffers, freeing the resources used by the buffer.
        Buffers which are attached to a source can not be deleted. See alSourcei and
        alSourceUnqueueBuffers for information on how to detach a buffer from a source.

    Args:
        n: the number of buffers to be deleted.
        buffers: pointer to an array of buffer names identifying the buffers to be
            deleted.
    """
    pass

@native_impl(ALuint, ALenum, POINTER(ALvoid), ALsizei, ALsizei)
def alBufferData(buffer, format, data, size, freq):
    """This function fills a buffer with audio data. All the pre-defined formats are PCM data, but
        this function may be used by extensions to load other data types as well. 

    Args:
        buffer: buffer name to be filled with data.
        format: format type from among the following:
            AL_FORMAT_MONO8
            AL_FORMAT_MONO16
            AL_FORMAT_STEREO8
            AL_FORMAT_STEREO16.
        data: pointer to the audio data.
        size: the size of the audio data in bytes.
        freq: the frequency of the audio data.
    """
    pass

@native_impl(returns=ALenum)
def alGetError():
    """This function returns the current error state and then clears the error state. 

    Returns:
        An Alenum representing the error state. When an OpenAL error occurs, the
        error state is set and will not be changed until the error state is retrieved using alGetError.
        Whenever alGetError is called, the error state is cleared and the last state (the current
        state when the call was made) is returned. To isolate error detection to a specific portion
        of code, alGetError should be called before the isolated section to clear the current error
        state.
    """
    pass