import unittest

from OrcLib.LibTest import OrcTest
from OrcDriver.Web.service import DriverService


class TestService(unittest.TestCase):

    def test_page_get_url_01(self):
        """
        Get page usl
        :return:
        """
        OrcTest.test_print_begin()

        _service = DriverService()
        _res = _service.page_get_url("3100000001")

        OrcTest.test_print_result(_res, "Page url")

        OrcTest.test_print_end()

    def test_page_get_url_02(self):
        """
        Page is not exists
        :return:
        """
        OrcTest.test_print_begin()

        _service = DriverService()
        _res = _service.page_get_url("3300000001")

        OrcTest.test_print_result(_res, "Page url")

        OrcTest.test_print_end()

    def test_get_widget_def_01(self):
        """
        Get widget definition
        :return:
        """
        OrcTest.test_print_begin()

        _service = DriverService()
        _res = _service.widget_get_definition("3200000003")

        OrcTest.test_print_result(_res, "Widget definition")

        OrcTest.test_print_end()

    def test_get_widget_def_02(self):
        """
        Widget is not exists
        :return:
        """
        OrcTest.test_print_begin()

        _service = DriverService()
        _res = _service.widget_get_definition("3300000001")

        OrcTest.test_print_result(_res, "Widget definition")

        OrcTest.test_print_end()

    def test_get_widget_det_01(self):
        """
        Get widget detail
        :return:
        """
        OrcTest.test_print_begin()

        _service = DriverService()
        _res = _service.widget_get_definition("3200000003")

        OrcTest.test_print_result(_res, "Widget detail")

        OrcTest.test_print_end()

    def test_get_widget_det_02(self):
        """
        Widget is not exists
        :return:
        """
        OrcTest.test_print_begin()

        _service = DriverService()
        _res = _service.widget_get_definition("3300000003")

        OrcTest.test_print_result(_res, "Widget detail")

        OrcTest.test_print_end()
