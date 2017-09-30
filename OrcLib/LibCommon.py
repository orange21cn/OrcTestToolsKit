# coding=utf-8
import re
import sys
import time
import random


def is_equal_str(str_a, str_b):
    """
    判断字符串相等，None 作为空串处理
    :param str_a: string，参数 A
    :param str_b: string，参数 B
    :return: bool
    """
    if str_a is None:
        str_a = ""
    if str_b is None:
        str_b = ""

    return str_a == str_b


def is_true(p_str):
    return "TRUE" == p_str


def is_false(p_str):
    return "FALSE" == p_str


def is_null(p_str):
    """
    判断字符串为空，None 作为空串处理
    :param p_str: string 输入参数，字符串
    :return: bool
    """
    return (p_str is None) or\
           ("" == p_str) or\
           ("None" == p_str)


def set_default_encoding():
    """
    设置默认字符集
    :return:
    """
    reload(sys)
    sys.setdefaultencoding('utf-8')


class OrcCovert:

    def __init__(self):
        pass

    @staticmethod
    def time2str(p_time):
        try:
            _res = p_time.strftime("%Y-%m-%d %H:%M:%S")
        except (AttributeError, TypeError):
            _res = None
        return _res

    @staticmethod
    def str2time(p_str):
        try:
            _res = time.mktime(time.strptime(p_str, "%Y-%m-%d %H:%M:%S"))
        except (AttributeError, TypeError):
            _res = None
        return _res


class OrcString(object):

    def __init__(self):

        object.__init__(self)

    @staticmethod
    def get_data_str():
        return time.strftime("%Y%m%d")

    @staticmethod
    def get_long_str():
        """
        生成一个长的日期字符串,至毫秒,低重复率
        :return:
        """
        return time.strftime("%Y%m%d%H%M%S")

    @staticmethod
    def fetch_string(p_start, p_end, p_str):
        """
        根据起始和结束字符串截取一个字符串,找不到返回 None
        :param p_start:
        :type p_start: str
        :param p_end:
        :type p_end: str
        :param p_str:
        :type p_str: str
        :return:
        """
        start_index = p_str.find(p_start)
        end_index = p_str.find(p_end)
        if (0 >= start_index) or (0 >= end_index):
            return ''

        start_index += len(p_start)

        return p_str[start_index:end_index].strip()

    @staticmethod
    def random_by_len(p_length):
        """
        获取指定长度随机数
        :param p_length:
        :return:
        """
        try:
            num = int(p_length)
        except (ValueError, TypeError):
            return ''

        if 0 >= num:
            return ''

        return random.randint(10**(num - 1), (10**num - 1))

    @staticmethod
    def trim_str_list(p_list):
        """
        list 中所有的 string 进行 trim 操作
        :return:
        """
        for _index in range(len(p_list)):
            p_list[_index] = re.sub('^[ \t]*', '', p_list[_index])
            p_list[_index] = re.sub('[ \t]*$', '', p_list[_index])
