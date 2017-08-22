# coding=utf-8
import unittest
from OrcLib.LibTest import OrcTest
from OrcApi.Run.RunDefMod import RunDefMod


class TestModel(unittest.TestCase):

    def test_add_01(self):
        """
        增加测试集目录
        :return:
        """
        OrcTest.test_print_begin()

        from OrcApi.Run.RunData import RunData

        obj = RunData()

        res = obj.get_case_list('200000008')
        for i in res:
            print i

        OrcTest.test_print_end()