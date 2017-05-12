# coding=utf-8
import abc
import json
import socket
from OrcLib.LibLog import OrcLog

_logger = OrcLog('basic.lib.lib_program')


def orc_singleton(cls):
    """
    单例
    :param cls:
    :return:
    """
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)

        return instances[cls]

    return _singleton


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


# class Singleton(object):
#
#     # 定义静态变量实例
#     __instance = None
#
#     def __init__(self):
#         pass
#
#     def __new__(cls, *args, **kwargs):
#         if not cls.__instance:
#             try:
#                 Lock.acquire()
#                 # double check
#                 if not cls.__instance:
#                     cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
#             finally:
#                 Lock.release()
#         return cls.__instance

class OrcDataStruct(object):
    def __init__(self):
        pass

    @staticmethod
    def iterator_reversed_list(p_list):
        """
        反向数组迭代器,用于反向输出数组元素
        :param p_list:
        :return:
        """
        assert isinstance(p_list, list)

        len_list = len(p_list)

        for _index in range(len_list):
            yield p_list[len_list - _index - 1]


class OrcSocketServer(object):
    def __init__(self, p_ip, p_port):

        self._logger = OrcLog('basic.lib_program.mem_server')

        self._ip = p_ip
        self._port = p_port

    def start(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._ip, self._port))
        sock.listen(1)

        while True:

            connection, address = sock.accept()

            try:
                connection.settimeout(5)

                _cmd = connection.recv(1024)

                self._logger.info('%s input: %s' % (self.start.__name__, _cmd))

                # 多进程不起作用,暂时用单进程
                # task = multiprocessing.Process(target=self.execute, args=(_cmd,))
                # result = task.start()
                # task.join()
                result = self.execute(_cmd)

                if "quit" == result:
                    break

                self._logger.info('%s result: %s' % (self.start.__name__, result))

                connection.send(str(result))

            except socket.timeout:
                self._logger.error("time out")
                connection.send(str(False))

            except Exception, err:
                self._logger.error(err)
                connection.send(str(False))

            connection.close()

    @abc.abstractmethod
    def execute(self, p_cmd):
        """
        执行函数
        :param p_cmd:
        :return:
        """
        pass


# ---- Type ----
class OrcSwitch(object):
    """
    模拟 switch 关键字
    """
    def __init__(self, p_def):

        object.__init__(self)

        self._operator = p_def

    def run(self, p_flag, *args, **kwargs):

        try:
            return self._operator[p_flag](*args, **kwargs)
        except (TypeError, KeyError, Exception):
            _logger.error('File %s, class %s, func %s, parameter %s %s' %
                          (__name__, 'OrcSwitch', 'run', args, kwargs))
            return None


class OrcMap(object):
    """
    dict 类型 none 判断
    """
    def __init__(self, p_data, p_default=None):

        self._data = p_data
        self._default = p_default

    def value(self, p_key, p_default=None):

        self._default = p_default

        if not isinstance(self._data, dict):
            return self._default

        return self._default if p_key not in self._data else self._data[p_key]


class OrcEnum(set):
    """
    Enum 类型
    """
    def __getattr__(self, name):

        if name in self:
            return name()

        raise AttributeError


class OrcFactory(object):

    def __init__(self):
        object.__init__(self)

    @staticmethod
    def create_dict(p_data):
        return OrcMap(p_data)

    @staticmethod
    def create_switch(p_def):
        return OrcSwitch(p_def)

    @staticmethod
    def create_enum(p_def):
        return OrcEnum(p_def)
