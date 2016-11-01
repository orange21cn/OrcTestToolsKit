# coding=utf-8
import unittest
from OrcLib.LibTest import OrcTest
from OrcApi.Run.RunCore import RunCore


class TestModel(unittest.TestCase):
    def test_add_01(self):
        """
        增加测试集目录
        :return:
        """
        OrcTest.test_print_begin()

        from OrcLib import get_config

        _configer = get_config()

        _home = _configer.get_option("DEFAULT", "root")
        _file = "%s/run_home/BATCH_1000000001/20161028154127/default.res" % _home
        _model = RunCore()

        _model.load_list(_file)

        OrcTest.test_print_result(_model.list)

        OrcTest.test_print_end()