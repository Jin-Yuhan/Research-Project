'''
author: Jin Yuhan
date: 2020-12-25 23:35:10
lastTime: 2021-02-03 20:40:59
'''

from arduino_api.binary_reader import BinaryReader
from serial import Serial

class ArduinoDataReceiver(object):
    """表示 Arduino 数据的接收器。

    Attributes:
        gravity: 重力加速度。
        float_ndigits: 浮点数小数点后保留的位数。
        package_flags: 数据包的标识位列表。
        package_body_size: 数据包包体（不包括标识位）的字节数。
    """
    def __init__(self, **kwargs):
        """初始化 ArduinoDataReceiver 实例。

        初始化一个具有指定参数的 ArduinoDataReceiver 实例。

        Args:
            kwargs: 可选的键值对参数。可选值如下：
                port: 串口。
                baudrate: 波特率。
                timeout: 接收超时前等待的时间跨度。
                gravity: 重力加速度。
                float_ndigits: 浮点数小数点后保留的位数。
                package_flags: 数据包的标识位列表。
                package_body_size: 数据包包体（不包括标识位）的字节数。
        """
        port = kwargs.get('port', None)
        baudrate = kwargs.get('baudrate', 9600)
        timeout = kwargs.get('timeout', 1)
        
        self.__serial = Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.gravity = kwargs.get('gravity', 9.8)
        self.float_ndigits = kwargs.get('float_ndigits', 4)
        self.package_flags = kwargs.get('package_flags', [0x55, 0x59])
        self.package_body_size = kwargs.get('package_body_size', 30)

    @property
    def port(self):
        """获取串口。"""
        return self.__serial.port
    
    @port.setter
    def port(self, value):
        """设置串口。"""
        self.__serial.port = value

    @property
    def baudrate(self):
        """获取波特率。"""
        return self.__serial.baudrate

    @baudrate.setter
    def baudrate(self, value):
        """设置波特率。"""
        self.__serial.baudrate = value

    @property
    def timeout(self):
        """获取接收超时前等待的时间跨度。"""
        return self.__serial.timeout

    @timeout.setter
    def timeout(self, value):
        """设置接收超时前等待的时间跨度。"""
        self.__serial.timeout = value

    @property
    def active(self):
        """获取是否已经打开串口。"""
        return self.__serial.isOpen()

    def __read_package_flag(self):
        data = self.__serial.read(1)
        
        if not data:
            raise TimeoutError("Receive package_flag timeout.")
        return data[0]

    def __wait_for_package(self):
        flags = [self.__read_package_flag() for _ in self.package_flags]

        while flags != self.package_flags:
            flags.pop(0)
            flags.append(self.__read_package_flag())
            

    def __package_to_list(self, package_buffer):
        result = []
        reader = BinaryReader(package_buffer)
        
        accel = reader.read_float_many(
            3, lambda v: round(v * 16 * self.gravity, self.float_ndigits)
        )
        angular_v = reader.read_float_many(
            3, lambda v: round(v * 2000, self.float_ndigits)
        )
        rotation = reader.read_float_many(
            3, lambda v: round(v * 180, self.float_ndigits)
        )
        left_p = reader.read_int_many(
            3, lambda v: float(v), signed=False
        )
        right_p = reader.read_int_many(
            3, lambda v: float(v), signed=False
        )

        result.extend(accel)
        result.extend(angular_v)
        result.extend(rotation)
        result.extend(left_p)
        result.extend(right_p)
        return result

    def receive(self):
        """接收数据。

        从串口中接收一个来自 Arduino 的数据包，并返回。
        在接收成功或超时前，会阻塞当前线程。

        Returns:
            一个列表，依次是：
                加速度X，加速度Y，加速度Z，
                角速度X，角速度Y，角速度Z，
                姿态角X，姿态角Y，姿态角Z，
                左脚压力0，左脚压力1，左脚压力2，
                右脚压力0，右脚压力1，右脚压力2。

        Raises:
            TimeoutError: 接收数据包超时。
            PortNotOpenError: 串口未打开。
            SerialException: 串口错误。
        """
        self.__wait_for_package()
        buffer = self.__serial.read(self.package_body_size)
        if len(buffer) != self.package_body_size:
            raise TimeoutError("Receive package_body timeout.")
        return self.__package_to_list(buffer)

    def start(self):
        """开始接收数据。"""
        self.__serial.open()

    def stop(self):
        """停止接收数据。"""
        self.__serial.close()

    def __enter__(self):
        self.__serial.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        self.__serial.__exit__(*args, **kwargs)
