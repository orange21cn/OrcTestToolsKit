# coding=utf-8
import traceback
import unittest

from OrcApi.Driver.Web.WidgetDefMod import WidgetDefMod
from OrcLib.LibNet import OrcResource

from OrcLib.LibTest import OrcTest


class TestSearch(unittest.TestCase):

    def test_usr_search_01(self):
        """
        Test search
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDefMod()
        _res = _handle.usr_search({"id": "3200000001"})
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_usr_search_02(self):
        """
        Test search
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDefMod()
        _res = _handle.usr_search({"id": "3200000004"})
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_usr_search_all_01(self):
        """
        Test search all
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDefMod()
        _res = _handle.usr_search_all({"id": "3200000001"})
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_usr_search_all_02(self):
        """
        Not exists
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDefMod()
        _res = _handle.usr_search_all({"id": "3200000004"})
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_usr_search_tree_01(self):
        """
        Search tree
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDefMod()
        _res = _handle.usr_search_path("3200000003")
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_usr_search_tree_02(self):
        """
        Not exists
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDefMod()
        _res = _handle.usr_search_path("3200000004")
        for i in _res:
            OrcTest.test_print_result(i)

        OrcTest.test_print_end()

    def test_model_get_path(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = WidgetDefMod()
        _res = _handle.usr_get_path("120300000000005")
        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_api_usr_search(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = {'id': '1004'}
        i_url = 'http://127.0.0.1:5000/WidgetDef/usr_search'

        pass

        OrcTest.test_print_end()

    def test_api_usr_get_path_001(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = ["120300000000005", "120300000000003"]
        i_url = 'http://127.0.0.1:5000/WidgetDef/usr_get_path'

        pass

        OrcTest.test_print_end()

    def test_api_usr_get_path_002(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = "120300000000005"
        i_url = 'http://127.0.0.1:5000/WidgetDef/usr_get_path'

        pass

        OrcTest.test_print_end()


class TestUpDown(unittest.TestCase):

    def test_bus_det_up(self):
        """
        测试上移
        :return:
        """
        OrcTest.test_print_begin()

        from OrcApi.Driver.Web.WidgetBus import WidgetDetBus

        bus = WidgetDetBus()
        print bus.bus_up(3400000003)

        OrcTest.test_print_end()

    def test_bus_det_down(self):
        """
        测试下移
        :return:
        """
        OrcTest.test_print_begin()

        from OrcApi.Driver.Web.WidgetBus import WidgetDetBus

        bus = WidgetDetBus()
        print bus.bus_down(3400000003)

        OrcTest.test_print_end()

    def test_api_det_up(self):
        """
        测试上移
        :return:
        """
        OrcTest.test_print_begin()

        res = OrcResource("WidgetDet")

        OrcTest.test_print_result(res.post(path=3400000003, parameter=dict(cmd="up")))

        OrcTest.test_print_end()

    def test_api_det_down(self):
        """
        测试上移
        :return:
        """
        OrcTest.test_print_begin()

        res = OrcResource("WidgetDet")

        OrcTest.test_print_result(res.post(path=3400000003, parameter=dict(cmd="down")))

        OrcTest.test_print_end()
