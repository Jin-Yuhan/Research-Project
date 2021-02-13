# -*- coding:utf-8  -*-

'''
author: Jin Yuhan
date: 2021-02-08 17:28:48
lastTime: 2021-02-13 19:10:14
'''

from openal.al import *
from os.path import basename
import wave

def load_from_file(file_path):
    """从指定文件中加载一个音频。

    Args:
        file_path (str): 文件路径。

    Returns:
        AudioClip: 如果成功则返回一个音频对象，否则返回None。
    """
    try:
        ext = file_path.split(".")[-1]
        if ext == 'wav':
            return WaveAudioClip(file_path)
    except:
        pass
    return None

class AudioClip(object):
    """表示一个音频。"""
    FORMAT_MAP = {
        (1, 8): AL_FORMAT_MONO8,
        (2, 8): AL_FORMAT_STEREO8,
        (1, 16): AL_FORMAT_MONO16,
        (2, 16): AL_FORMAT_STEREO16,
    }
    
    def __init__(self, name, channels, frequency, length, bitrate, data):
        """初始化一个音频对象。

        Args:
            name (str): 音频的名称。
            channels (int): 音频的声道数。
            frequency (int): 音频的采样频率（以赫兹为单位）。
            length (float): 音频的长度（以秒为单位）。
            bitrate (int): 音频的比特率。
            data (bytes): 音频的字节数据。
        """
        self._name = name
        self._channels = channels
        self._frequency = frequency
        self._length = length
        self._buffer = ALuint(0)
        alGenBuffers(1, self._buffer)
        format = AudioClip.FORMAT_MAP[(channels, bitrate)]
        alBufferData(self._buffer, format, data, len(data), frequency)

    def __del__(self):
        alDeleteBuffers(1, self._buffer)
    
    @property
    def name(self) -> str:
        """音频的名称。"""
        return self._name

    @property
    def channels(self) -> int:
        """音频的声道数。"""
        return self._channels

    @property
    def frequency(self) -> int:
        """音频的采样频率（以赫兹为单位）。"""
        return self._frequency

    @property
    def length(self) -> float:
        """音频的长度（以秒为单位）。"""
        return self._length

    @property
    def buffer(self) -> ALuint:
        """获取音频的alBuffer。"""
        return self._buffer

class WaveAudioClip(AudioClip):
    def __init__(self, file_path):
        with wave.open(file_path) as wavefp:
            name = basename(file_path)
            channels = wavefp.getnchannels()
            framerate = wavefp.getframerate()
            frames = wavefp.getnframes()
            length = frames / float(framerate)
            bitrate = wavefp.getsampwidth() * 8
            data = wavefp.readframes(frames)
            super().__init__(name, channels, framerate, length, bitrate, data)
    