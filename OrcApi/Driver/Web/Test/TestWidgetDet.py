import traceback
import unittest

from OrcLib.LibTest import OrcTest
from OrcLib.LibException import OrcPostFailedException


class TestModel(unittest.TestCase):

    def test_model_usr_search(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        pass

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
            # result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()
