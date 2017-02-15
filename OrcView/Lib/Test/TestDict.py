import unittest

from OrcLib.LibTest import OrcTest
from OrcView.Lib.LibDict import LibDict


class TestDict(unittest.TestCase):

    def test_get_dict_01(self):
        """
        test get dict
        :return:
        """
        OrcTest.test_print_begin()

        _obj = LibDict()

        OrcTest.test_print_result(_obj.get_dict("item_type"))

        OrcTest.test_print_end()

    def test_get_type_01(self):
        """
        test get type by id
        :return:
        """
        OrcTest.test_print_begin()

        _obj = LibDict()

        OrcTest.test_print_result(_obj.get_widget_type(p_id="30001").to_json())

        OrcTest.test_print_end()

    def test_get_type_02(self):
        """
        test get type by id, id is not exists
        :return:
        """
        OrcTest.test_print_begin()

        _obj = LibDict()

        OrcTest.test_print_result(_obj.get_widget_type(p_id="40001"))

        OrcTest.test_print_end()

    def test_get_type_03(self):
        """
        test get type by name
        :return:
        """
        OrcTest.test_print_begin()

        _obj = LibDict()

        OrcTest.test_print_result(_obj.get_widget_type(p_name="WINDOW").to_json())

        OrcTest.test_print_end()

    def test_get_type_04(self):
        """
        test get type by name, name is not exists
        :return:
        """
        OrcTest.test_print_begin()

        _obj = LibDict()

        OrcTest.test_print_result(_obj.get_widget_type(p_name="WINDOWs"))

        OrcTest.test_print_end()

    def test_select_dict(self):
        """
        test get type by name, name is not exists
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Lib.LibView import SelectDictionary

        OrcTest.display_widget(SelectDictionary, 'test_env', True)

        OrcTest.test_print_end()
