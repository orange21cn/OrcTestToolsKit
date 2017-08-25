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

        from OrcView.Driver.Cmd.DataFlagSelector import DataFlagView1

        OrcTest.display_widget(DataFlagView1)

        OrcTest.test_print_end()

    def test_page_def(self):
        """
        增加测试集目录
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.Page.PageSelector import PageSelector

        OrcTest.display_widget(DataFlagView1)

        OrcTest.test_print_end()