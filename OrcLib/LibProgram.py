# coding=utf-8
import abc
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


class OrcDataStruct(object):
    """

    """
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


class OrcDefaultDict(object):
    """
    有默认值字典
    """
    def __init__(self, data_dict=None, default=None, func=None):

        # 字典数据
        self._data = dict()

        # 执行函数
        self._func = func

        # 默认值
        self._default = default

        if isinstance(data_dict, dict):
            self._data = data_dict

    def value(self, p_key, p_default=None):
        """
        值
        :param p_key:
        :param p_default:
        :return:
        """
        self._default = p_default

        if not isinstance(self._data, dict):
            return self._default

        if p_key not in self._data:
            return self._default

        if self._func is None:
            return self._data[p_key]
        else:
            return self._func(self._data[p_key])

    def add(self, p_key, p_value):
        """
        增加一条数据
        :param p_key:
        :param p_value:
        :return:
        """
        self._data[p_key] = p_value

    def delete(self, p_key):
        """
        删除
        :param p_key:
        :return:
        """
        self._data.pop(p_key)

    def items(self):
        """
        迭代器
        :return:
        """
        return self._data.items()

    def keys(self):
        """
        迭代 Key
        :return:
        """
        return self._data.keys()

    def dict(self):
        """
        返回字典
        :return:
        """
        return self._data


class OrcOrderedDict(object):
    """
    有序字典
    """
    def __init__(self):

        object.__init__(self)

        # 保存数据
        self._order = list()

        # 保存字典
        self._data = OrcDefaultDict()

    def value(self, p_key):
        """
        获取值
        :param p_key:
        :return:
        """
        return self._data.value(p_key)

    def value_by_index(self, p_index):
        """
        通过索引获取值
        :param p_index:
        :type p_index: int
        :return:
        """
        try:
            key = self._order[p_index]
            return self._data.value(key)
        except(TypeError, IndexError):
            _logger.error("Wrong index %s" % p_index)
            return None

    def append(self, p_key, p_value):
        """
        增加一个值
        :return:
        """
        self._order.append(p_key)
        self._data.add(p_key, p_value)

    def pop(self):
        """
        删除一个值
        :return:
        """
        key = self._order[-1]
        self._order.pop()
        self._data.delete(key)

    def insert(self, p_index, p_key, p_value):
        """
        插入一个值
        :param p_value:
        :param p_key:
        :param p_index:
        :return:
        """
        self._order.insert(p_index, p_key)
        self._data.add(p_key, p_value)

    def delete(self, p_index):
        """
        删除一个值
        :param p_index:
        :return:
        """
        self._order.remove(self._order[p_index])

    def items(self):
        """
        迭代器
        :return:
        """
        for _key in self._order:
            yield _key, self._data.value(_key)

    def keys(self):
        """
        迭代 key
        :return:
        """
        for _key in self._order:
            yield _key

    def dict(self):
        """
        输出 dict
        :return:
        """
        return self._data.dict()


class OrcEnum(set):
    """
    Enum 类型
    """
    def __getattr__(self, name):

        if name in self:
            return name

        raise AttributeError


class OrcFactory(object):

    def __init__(self):
        object.__init__(self)

    @staticmethod
    def create_default_dict(data=None, default=None, func=None):
        return OrcDefaultDict(data, default, func)

    @staticmethod
    def create_switch(p_def):
        return OrcSwitch(p_def)

    @staticmethod
    def create_enum(p_def):
        return OrcEnum(p_def)

    @staticmethod
    def create_ordered_dict():
        return OrcOrderedDict()
