# coding=utf-8
import os
from OrcLib.LibNet import get_config

_configer = get_config()


def get_theme(p_flag):
    """
    获取主题
    :param p_flag:
    :return:
    """
    theme_folder = _configer.get_option("DEFAULT", "root")
    theme_file = '%s/OrcView/Style/default/%s.qss' % (theme_folder, p_flag)

    if not os.path.exists(theme_file):
        return ""

    qss_file = open(theme_file)
    theme = qss_file.read()
    qss_file.close()

    return theme
