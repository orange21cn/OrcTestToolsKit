import traceback
import unittest

from OrcDriver.Web import WidgetDetHandle
from OrcLib import OrcTest
from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibNet import orc_invoke


class TestModel(unittest.TestCase):

    def test_model_usr_search(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDetHandle()
        _res = _handle.usr_search({"id": "1005"})
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_api_usr_search(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = {'id': '1005'}
        i_url = 'http://127.0.0.1:5000/WidgetDet/usr_search'

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()
