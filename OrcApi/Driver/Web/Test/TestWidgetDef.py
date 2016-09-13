import traceback
import unittest

from OrcDriver.Web.WidgetDefModel import WidgetDefHandle
from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibNet import orc_invoke

from OrcLib import OrcTest


class TestModel(unittest.TestCase):

    def test_model_usr_search(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDefHandle()
        _res = _handle.usr_search({"id": "1004"})
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_model_get_path(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDefHandle()
        _res = _handle.usr_get_path("120300000000005")
        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_api_usr_search(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = {'id': '1004'}
        i_url = 'http://127.0.0.1:5000/WidgetDef/usr_search'

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()

    def test_api_usr_get_path_001(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = ["120300000000005", "120300000000003"]
        i_url = 'http://127.0.0.1:5000/WidgetDef/usr_get_path'

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()

    def test_api_usr_get_path_002(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = "120300000000005"
        i_url = 'http://127.0.0.1:5000/WidgetDef/usr_get_path'

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()
