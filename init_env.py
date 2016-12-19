# coding=utf-8
import os
from OrcLib.LibConfig import OrcConfig


# 初始化 home 目录
home_path = os.path.dirname(os.path.dirname(__file__))

for _mod in ('default', 'database', 'log'):

    cfg_file = "%s/config/%s.cfg" % (home_path, _mod)

    if os.path.exists(cfg_file):

        _cfg = OrcConfig(cfg_file)
        _cfg.set_option("DEFAULT", "root", home_path)
