import traceback
import unittest

from OrcApi.Batch.BatchDefModel import BatchDefModel
from OrcLib.LibDatabase import TabCaseDef
from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibNet import orc_invoke
from OrcLib.LibNet import OrcInvoke

from OrcLib.LibTest import OrcTest


class TestTab(unittest.TestCase):

    def test_get_root(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        test = BatchDefModel()
        ttt = TabCaseDef()
        ttt.id = '2'
        i = test._get_root(ttt)
        OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_get_tree(self):
        """
        Test get tree
        :return:
        """
        OrcTest.test_print_begin()

        test = BatchDefModel()
        ttt = TabCaseDef()
        ttt.id = '1'
        i = test._get_tree(ttt)
        for a in i:
            OrcTest.test_print_result(a.to_json())

        OrcTest.test_print_end()

    def test_table(self):
        """
        Test function with no parameter
        :return:
        """
        OrcTest.test_print_begin()

        test = BatchDefModel()

        for i in test.usr_search():
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_with_parameter(self):
        """
        Test with parameter id
        :return:
        """
        OrcTest.test_print_begin()

        test = BatchDefModel()

        for i in test.usr_search({'id': '1001000000000003'}):
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()


class TestUserAdd(unittest.TestCase):

    def test_user_add_01(self):

        OrcTest.test_print_begin()

        test = BatchDefModel()

        i = test.usr_add({'batch_name': '1', 'batch_desc': '2'})
        OrcTest.test_print_result(i)

        OrcTest.test_print_end()


class TestModify(unittest.TestCase):

    def test_modify_001(self):

        OrcTest.test_print_begin()

        test = BatchDefModel()

        test.usr_modify({'id': '1001000000000003', 'pid': '1001000000000001'})

        OrcTest.test_print_end()


class TestDelete(unittest.TestCase):

    def test_delete_001(self):

        OrcTest.test_print_begin()

        test = BatchDefModel()

        test.usr_delete({"list": ['1001000000000007']})

        OrcTest.test_print_end()


class TestBatchDef(unittest.TestCase):

    def test_get_data_02(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = {'id': '1001000000000003'}
        i_url = 'http://127.0.0.1:5000/BatchDef/usr_search'

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()

    def test_get_batch(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        test = BatchDefModel()

        _res = test.usr_get_path("1001000000000003")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()


class TestFunc(unittest.TestCase):

    def test_get_no(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = '1000000001'
        i_url = 'http://127.0.0.1:5000/BatchDef/usr_get_no'

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()


class TestBatchDefRest(unittest.TestCase):

    def test_window_post_01(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _invoke = OrcInvoke()

        _url = 'http://127.0.0.1:5000/api/1.0/BatchDef/171602024'
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

        _url = 'http://127.0.0.1:5000/api/1.0/BatchDef/1000000001'
        _para = None

        try:
            result = _invoke.get(_url, _para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()
