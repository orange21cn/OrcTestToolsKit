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


def init_log():
    """
    获取配置类
    :return:
    """
    _path = os.path.dirname(os.path.dirname(__file__))
    _file = "%s/config/log.cfg" % _path

    if os.path.exists(_file):

        _cfg = OrcConfig(_file)
        _cfg.set_option("DEFAULT", "root", _path)

    logging.config.fileConfig(_file)
