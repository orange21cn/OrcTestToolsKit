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
            self.__conf.read(self.__file)
            _res = self.__conf.get(p_sec, p_key)
        except (NoOptionError, NoSectionError, TypeError):
            _res = None

        return _res

    def get_options(self, p_sec):
        """
        获取配置
        :param p_sec: section
        :return: None if section is not exists
        """
        try:
            self.__conf.read(self.__file)
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
        if self.__conf.has_section(p_sec):

            _file = open(self.__file, "w")

            self.__conf.set(p_sec, p_key, p_value)
            self.__conf.write(_file)

            _file.close()

            _rtn = True

        return _rtn

    def del_option(self, p_sec, p_key):
        """
        删除配置项
        :param p_sec:
        :param p_key:
        :return:
        """
        _file = open(self.__file, "w")
        self.__conf.remove_option(p_sec, p_key)
        self.__conf.write(_file)

        _file.close()

    def add_section(self, p_sec):
        """
        增加配置项
        :param p_sec:
        :return:
        """
        if self.__conf.has_section(p_sec):
            return

        self.__conf.add_section(p_sec)

    def del_section(self, p_sec):
        """
        删除配置项
        :param p_sec:
        :return:
        """
        _file = open(self.__file, "w")
        self.__conf.remove_section(p_sec)
        self.__conf.write(_file)

        _file.close()

    def get_sections(self):
        """
        获取所有 section
        :return:
        """
        return self.__conf.sections()
