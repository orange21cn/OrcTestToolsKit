import sys
import unittest

from PySide.QtGui import QApplication
from OrcView.Driver.Web.WebMain import ViewWebMain
from OrcLib.LibTest import OrcTest


class TestWebMain(unittest.TestCase):

    def test_web_main(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _main = QApplication(sys.argv)
        _view = ViewWebMain()
        _view.show()

        _main.exec_()

        OrcTest.test_print_end()


class TestService(unittest.TestCase):

    def test_get_page_def_01(self):
        """
        Test page definition
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.service import WebMainService

        _service = WebMainService()
        _res = _service.get_page_def("3000000001")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_page_def_02(self):
        """
        Test page definition, page is not exists
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.service import WebMainService

        _service = WebMainService()
        _res = _service.get_page_def("4300000003")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_page_det_01(self):
        """
        Test page detail
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.service import WebMainService

        _service = WebMainService()
        _res = _service.get_page_det("3100000001")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_page_det_02(self):
        """
        Test page detail, page is not exists
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.service import WebMainService

        _service = WebMainService()
        _res = _service.get_page_det("4100000001")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_widget_def_01(self):
        """
        Test widget definition
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.service import WebMainService

        _service = WebMainService()
        _res = _service.get_widget_def("3300000003")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_widget_def_02(self):
        """
        Test widget definition, widget is not exists
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.service import WebMainService

        _service = WebMainService()
        _res = _service.get_widget_def("4300000003")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_widget_det_01(self):
        """
        Test widget detail
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.service import WebMainService

        _service = WebMainService()
        _res = _service.get_widget_det("3400000001")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_widget_det_02(self):
        """
        Test widget definition, widget is not exists
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.service import WebMainService

        _service = WebMainService()
        _res = _service.get_widget_det("4300000003")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()
