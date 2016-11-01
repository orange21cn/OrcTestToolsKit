import traceback
import unittest

from OrcApi.Driver.Web.PageDefModel import PageDefModel
from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibNet import orc_invoke

from OrcLib.LibTest import OrcTest


class TestModel(unittest.TestCase):

    def test_usr_search(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = PageDefModel()
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

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()

    def test_usr_get_flag(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _para = {'id': '3000000001'}
        _url = 'http://127.0.0.1:5000/PageDef/usr_get_flag'

        try:
            result = orc_invoke(_url, _para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()
