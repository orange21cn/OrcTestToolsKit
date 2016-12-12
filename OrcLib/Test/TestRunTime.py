# coding=utf-8
import unittest
from OrcLib.LibTest import OrcTest
from OrcLib.LibRunTime import Runtime


class TestRunTime(unittest.TestCase):
    """
    运行时临时数据管理
    """
    def test_add_value(self):
        """
        新增一条数据
        """
        OrcTest.test_print_begin()

        run_time = Runtime("test_01")
        result = run_time.add_value(dict(data_flag="env", data_value="test"))

        OrcTest.test_print_result(result)

        OrcTest.test_print_begin()

    def test_set_value(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        run_time = Runtime("test_01")
        run_time.set_value("env", "abc")

        OrcTest.test_print_begin()

    def test_get_value(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        run_time = Runtime("test_01")
        result = run_time.get_value("env")

        OrcTest.test_print_result(result)

        OrcTest.test_print_begin()

    def test_get_values(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        run_time = Runtime("test_01")
        result = run_time.get_values("env")

        OrcTest.test_print_result(result)

        OrcTest.test_print_begin()

    def test_del_value_01(self):
        """
        删除一条数据
        """
        OrcTest.test_print_begin()

        run_time = Runtime("test_01")
        result = run_time.del_value("env", 1)

        OrcTest.test_print_result(result)

        OrcTest.test_print_begin()

    def test_del_value_02(self):
        """
        删除时 index 超出范围
        """
        OrcTest.test_print_begin()

        run_time = Runtime("test_01")
        result = run_time.del_value("env", 5)

        OrcTest.test_print_result(result)

        OrcTest.test_print_begin()

    def test_del_value_03(self):
        """
        删除时所有符合条件数据
        """
        OrcTest.test_print_begin()

        run_time = Runtime("test_01")
        result = run_time.del_value("env")

        OrcTest.test_print_result(result)

        OrcTest.test_print_begin()
