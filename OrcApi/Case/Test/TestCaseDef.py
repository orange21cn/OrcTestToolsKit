import traceback
import unittest

from OrcApi.Case.CaseDefMod import CaseDefMod
from OrcLib.LibException import OrcPostFailedException

from OrcLib.LibTest import OrcTest


class TestModel(unittest.TestCase):

    def test_model_search_path_001(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        test = CaseDefMod()
        ttt = test.usr_search_path('2000000004')
        OrcTest.test_print_result(ttt)

        OrcTest.test_print_end()

    def test_model_get_path_001(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        test = CaseDefMod()
        ttt = test.usr_get_path('110100000000079')
        OrcTest.test_print_result(ttt)

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_api_get_path_001(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        i_para = '2000000001'
        i_url = 'http://127.0.0.1:5000/CaseDef/usr_get_path'

        pass

        OrcTest.test_print_end()

    def test_api_get_path_002(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        i_para = ['110100000000079', '110100000000078']
        i_url = 'http://127.0.0.1:5000/CaseDef/usr_get_path'

        pass

        OrcTest.test_print_end()

    def test_api_case_def_get_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        pass

        OrcTest.test_print_end()
