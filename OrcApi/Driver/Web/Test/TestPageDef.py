import traceback
import unittest

from OrcApi.Driver.Web.PageDefMod import PageDefMod
from OrcLib.LibException import OrcPostFailedException

from OrcLib.LibTest import OrcTest


class TestModel(unittest.TestCase):

    def test_usr_search(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = PageDefMod()
        _res = _handle.usr_search({"id": "1002"})
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_usr_search(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = {'id': '1002'}
        i_url = 'http://127.0.0.1:5000/PageDet/usr_search'

        pass

        OrcTest.test_print_end()

    def test_usr_get_flag(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _para = {'id': '3000000001'}
        _url = 'http://127.0.0.1:5000/PageDef/usr_get_flag'

        pass

        OrcTest.test_print_end()
