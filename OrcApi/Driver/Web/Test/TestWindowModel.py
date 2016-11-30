# coding=utf-8
import traceback
import unittest

from OrcApi.Driver.Web.WindowDefMod import WindowDefMod

from OrcLib.LibNet import OrcInvoke
from OrcLib.LibTest import OrcTest
from OrcLib.LibException import OrcPostFailedException


class TestModel(unittest.TestCase):

    def test_usr_add_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WindowDefMod()

        _data = dict(window_id="1001",
                     window_mark="TEST_001",
                     window_desc=u"测试001",
                     comment=u"注释001")
        _res = _handle.usr_add(_data)

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_usr_update_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WindowDefMod()

        _data = dict(id="3200000009",
                     window_mark="TEST_002",
                     window_desc=u"测试002",
                     comment=u"注释002")
        _res = _handle.usr_update(_data)

        OrcTest.test_print_end()

    def test_usr_search_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WindowDefMod()
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

        _handle = WindowDefMod()
        _cond = dict(window_desc=u"测试")

        _res = _handle.usr_search(_cond)
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_window_post_01(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _invoke = OrcInvoke()

        _url = 'http://127.0.0.1:5000/api/1.0/windows/171602024'
        _para = dict(window_mark="TEST_001", window_desc="TEST_DESC_001", comment="TEST_COMMENT_001")

        try:
            result = _invoke.post(_url, _para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()

    def test_window_get_01(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _invoke = OrcInvoke()

        _url = 'http://127.0.0.1:5000/api/1.0/windows/171602023'
        _para = None

        try:
            result = _invoke.get(_url, _para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()

    def test_window_delete_01(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _invoke = OrcInvoke()

        _url = 'http://127.0.0.1:5000/api/1.0/windows/171602023'
        _para = None

        try:
            result = _invoke.delete(_url, _para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()

    def test_windows_get_01(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _invoke = OrcInvoke()

        _url = 'http://127.0.0.1:5000/api/1.0/windows'
        _para = dict(window_mark="TEST")

        try:
            result = _invoke.get(_url, _para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()

    def test_windows_delete_01(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _invoke = OrcInvoke()

        _url = 'http://127.0.0.1:5000/api/1.0/windows'
        _para = [171602001, 171602003, 171602005]

        try:
            result = _invoke.delete(_url, _para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()