# coding=utf-8
from importlib import import_module
import time
import re

# def import_mod(p_mod_name):
#     mod_obj = None
#     obj_db = DatabaseMag()
#     sql_str = "SELECT mod_path" \
#               "  FROM test_module" \
#               " WHERE mod_name = '" + p_mod_name + "'"
#
#     mod_path = obj_db.get_one(sql_str)[0]
#
#     if mod_path is not None:
#         mod_obj = import_module(mod_path, p_mod_name)
#
#     return mod_obj


class OrcDict():

    def __init__(self):
        pass

    @staticmethod
    def get_batch_path():
        pass

    @staticmethod
    def get_case_path():
        pass

    @staticmethod
    def get_dict_text():
        pass


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


def gen_date_str():
    return time.strftime("%Y%m%d%H%M%S")


def get_parent_no(p_no):
    """
    According to tree expression 10.11.12.13 function get the parent no.
    Remove the last part of expression ".13"
    If the expression is a root expression return None
    :param p_no: tree expression
    :return: parent expression
    """
    res_value = None

    if re.search('\.', p_no):
        res_value = re.sub('\.[^\.]*$', '', p_no)

    return res_value


def tuple2list(p_inp):
    if p_inp is not None:
        return list(str(member) for member in p_inp)
    else:
        return None


def time2char(p_inp):
    if is_null(p_inp):
        return ""
    else:
        return p_inp.strftime("%Y-%m-%d %H:%M:%S")


def add_quote(p_str):
    if type(p_str) is not int:
        return '\'' + p_str + '\''
    return '\'' + str(p_str) + '\''


def add_dquote(p_str):
    return '\'' + str(p_str) + '\''


class IndexStr:

    def __init__(self, p_seed):
        self.seed = p_seed

    def get_index(self):
        self.seed += 1
        return self.seed

    def get_date_index(self):
        self.seed += 1
        return gen_date_str() + "%s" % self.seed
