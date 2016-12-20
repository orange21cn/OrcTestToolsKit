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

        _model = RunDefMod()
        res = _model.usr_add("case", "2000000002", True)

        OrcTest.test_print_result(res)

        OrcTest.test_print_end()

    def test_add_02(self):
        """
        增加测试项目录及文件
        :return:
        """
        OrcTest.test_print_begin()

        _model = RunDefMod()
        res = _model.usr_add(dict(run_def_type="BATCH", id="1000000001", result=True))

        OrcTest.test_print_result(res)

        OrcTest.test_print_end()

    def test_search_01(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _model = RunDefMod()
        res = _model.usr_search()

        OrcTest.test_print_result(res)

        OrcTest.test_print_end()

    def test_search_02(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _model = RunDefMod()
        res = _model.usr_search(dict(id="8"))

        OrcTest.test_print_result(res)

        OrcTest.test_print_end()

    def test_delete_01(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _model = RunDefMod()
        res = _model.usr_delete(["batch_1000000007"])

        OrcTest.test_print_result(res)

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_add_01(self):
        """
        增加测试集目录
        :return:
        """
        OrcTest.test_print_begin()

        # invoker = OrcInvoke()

        # res = invoker.get("http://localhost:5004/api/1.0/RunDef")

        # OrcTest.test_print_result(res)

        OrcTest.test_print_end()
