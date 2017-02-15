# coding=utf-8
import os
import logging
import logging.config
from LibConfig import OrcConfig


def get_config(p_file=None):
    """
    获取配置类
    :param p_file:
    :return:
    """
    _path = os.path.dirname(os.path.dirname(__file__))
    _name = p_file

    if _name is None:
        _name = "default"

    _file = "%s/config/%s.cfg" % (_path, _name)

    if os.path.exists(_file):

        _cfg = OrcConfig(_file)
        _cfg.set_option("DEFAULT", "root", _path)

        return _cfg

    else:
        return None


def init_log(p_name=None):
    """
    获取配置类
    :param p_name: log 配置名 log-[name].cfg
    :return:
    """
    _path = os.path.dirname(os.path.dirname(__file__))

    _name = "" if p_name is None else ("-" + p_name)
    _file = "%s/config/log%s.cfg" % (_path, _name)

    if os.path.exists(_file):

        _cfg = OrcConfig(_file)
        _cfg.set_option("DEFAULT", "root", _path)

    logging.config.fileConfig(_file)
