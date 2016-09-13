import traceback
import unittest

from OrcLib.LibDatabase import TabCaseDef
from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibNet import orc_invoke
from OrcLib.LibTest import OrcTest

from OrcApi.Lib.Dictionory import DictHandle


class TestFunc(unittest.TestCase):

    def test_get_dict_text(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        test = DictHandle()
        _para = dict(flag="case_type", value="CASE")
        i = test.get_dict_text(_para)
        OrcTest.test_print_result(i)

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_get_dict_text(self):

        OrcTest.test_print_begin()

        i_para = dict(flag="case_type", value="CASE")
        i_url = 'http://127.0.0.1:5000/Lib/get_dict_text'

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()
