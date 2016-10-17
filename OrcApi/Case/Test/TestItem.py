import traceback
import unittest

from OrcBatch.BatchDefModel import BatchDefHandle
from OrcCase.ItemModel import ItemHandle
from OrcCase.StepDetModel import StepDetHandle
from OrcLib.LibDatabase import TabCaseDef
from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibNet import orc_invoke

from OrcLib import OrcTest


class TestTab(unittest.TestCase):

    def test_get_root(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        test = BatchDefHandle()
        ttt = TabCaseDef()
        ttt.id = '2'
        i = test.__get_root(ttt)
        OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_get_tree(self):
        """
        Test get tree
        :return:
        """
        OrcTest.test_print_begin()

        test = BatchDefHandle()
        ttt = TabCaseDef()
        ttt.id = '1'
        i = test.__get_tree(ttt)
        for a in i:
            OrcTest.test_print_result(a.to_json())

        OrcTest.test_print_end()

    def test_table(self):
        """
        Test function with no parameter
        :return:
        """
        OrcTest.test_print_begin()

        test = BatchDefHandle()

        for i in test.usr_search():
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_with_parameter(self):
        """
        Test with parameter id
        :return:
        """
        OrcTest.test_print_begin()

        test = BatchDefHandle()

        for i in test.usr_search({'id': '1001000000000003'}):
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()


class TestUserAdd(unittest.TestCase):

    def test_user_add_01(self):

        OrcTest.test_print_begin()

        test = BatchDefHandle()

        i = test.usr_add({'batch_name': '1', 'batch_desc': '2'})
        OrcTest.test_print_result(i)

        OrcTest.test_print_end()


class TestModify(unittest.TestCase):

    def test_modify_001(self):

        OrcTest.test_print_begin()

        test = BatchDefHandle()

        test.usr_update({'id': '1001000000000003', 'pid': '1001000000000001'})

        OrcTest.test_print_end()


class TestDelete(unittest.TestCase):

    def test_delete_001(self):

        OrcTest.test_print_begin()

        test = BatchDefHandle()

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


class TestBatchDet(unittest.TestCase):

    def test_search_001(self):
        """

        :return:
        """
        OrcTest.test_print_begin()

        i_para = {'id': '1002000000000002'}
        i_url = 'http://127.0.0.1:5000/CaseDet/usr_search'

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()


class TestStepItem(unittest.TestCase):

    def test_search_step_det_001(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        test = StepDetHandle()
        _res = test.usr_search({"step_id": "456"})
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_search_item_001(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        test = ItemHandle()
        _res = test.usr_list_search({"id": ['1001']})

        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_search_step_api_001(self):
        """

        :return:
        """
        OrcTest.test_print_begin()

        i_para = {'step_id': '456'}
        i_url = 'http://127.0.0.1:5000/StepDet/usr_search'

        try:
            result = orc_invoke(i_url, i_para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()
