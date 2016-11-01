# coding=utf-8
from ConfigParser import ConfigParser
from ConfigParser import NoOptionError
from ConfigParser import NoSectionError


class OrcConfig:
    """
    配置管理
    """
    def __init__(self, p_file):

        self.__file = p_file
        self.__conf = ConfigParser()
        self.__conf.read(p_file)

    def get_option(self, p_sec, p_key):
        """
        获取配置项
        :param p_sec:
        :param p_key:
        :return:
        """
        try:
            _res = self.__conf.get(p_sec, p_key)
        except (NoOptionError, NoSectionError):
            _res = None

        return _res

    def get_options(self, p_sec):
        """
        获取配置
        :param p_sec: section
        :return: None if section is not exists
        """
        try:
            _res = self.__conf.options(p_sec)
        except NoSectionError:
            _res = None

        return _res

    def set_option(self, p_sec, p_key, p_value):
        """
        设置配置项
        :param p_value: value
        :param p_key: option
        :param p_sec: section
        :return: False if set failed
        """
        _rtn = False

        # 如果配置项不存在返回失败
        if self.__conf.has_option(p_sec, p_key):

            _file = open(self.__file, "w")

            self.__conf.set(p_sec, p_key, p_value)
            self.__conf.write(_file)

            _file.close()

            _rtn = True

        return _rtn
