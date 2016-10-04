# coding=utf-8
import traceback
import unittest

from OrcApi.Driver.Web.WindowDefModel import WindowDefModel

from OrcLib.LibNet import orc_invoke
from OrcLib.LibTest import OrcTest


class TestModel(unittest.TestCase):

    def test_usr_add_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WindowDefModel()

        _data = dict(window_id="1001",
                     window_mark="TEST_001",
                     window_desc=u"测试001",
                     comment=u"注释001")
        _res = _handle.usr_add(_data)

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_usr_modify_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WindowDefModel()

        _data = dict(id="3200000009",
                     window_id="1002",
                     window_mark="TEST_002",
                     window_desc=u"测试002",
                     comment=u"注释002")
        _res = _handle.usr_modify(_data)

        OrcTest.test_print_end()

    def test_usr_search_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WindowDefModel()
        _cond = dict(id="3200000009")

        _res = _handle.usr_search(_cond)
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_usr_search_02(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WindowDefModel()
        _cond = dict(window_desc=u"测试")

        _res = _handle.usr_search(_cond)
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_usr_search(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        OrcTest.test_print_end()

    def test_usr_get_flag(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        # _para = {'id': '3000000001'}
        # _url = 'http://127.0.0.1:5000/PageDef/usr_get_flag'
        #
        # try:
        #     result = orc_invoke(_url, _para)
        #     OrcTest.test_print_result(result, 'result')
        # except OrcPostFailedException:
        #     traceback.print_exc()

        OrcTest.test_print_end()
