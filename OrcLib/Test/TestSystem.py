# coding=utf-8
import unittest

from OrcLib.LibTest import OrcTest


class TestRunTime(unittest.TestCase):
    """
    运行时临时数据管理
    """
    def test_add_value(self):
        """
        新增一条数据
        """
        OrcTest.test_print_begin()

        from OrcLib.LibSystem import OrcSystem

        print OrcSystem.get_platform()
        print OrcSystem.get_path('/etc/mysql')
        print OrcSystem.get_path('C:\Program File\abc\def')
        print OrcSystem.get_path(('c:\Windows', 'abc', 'def'))
        print OrcSystem.get_path(('c:'))
        print OrcSystem.get_path(('c:\Win', '/abc/def', 'g', 'a'))

        OrcTest.test_print_begin()
