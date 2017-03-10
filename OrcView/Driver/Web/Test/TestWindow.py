# coding=utf-8
import sys
import unittest

from OrcView.Driver.Web.WindowService import WindowDefService
from PySide.QtGui import QApplication

from OrcLib.LibTest import OrcTest


class TestService(unittest.TestCase):
    """

    """

    def test_add_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _service = WindowDefService()

        _data = dict(
            id="1716023001",
            window_id="1001",
            window_mark="TEST_001",
            window_desc=u"测试001",
            comment=u"注释001")
        _res = _service.mod_add(_data)

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_search_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _service = WindowService()

        _data = dict(
            id="1716023001")
        _res = _service.mod_search(_data)

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_update_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _service = WindowService()

        _data = dict(
            id=1716023001,
            window_mark="TEST_002",
            window_desc=u"测试002",
            comment=u"注释002")
        _res = _service.usr_update(_data)

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_delete_01(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _service = WindowService()

        _data = [171602012, 171602014]
        _res = _service.mod_delete(_data)

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()


class TestView(unittest.TestCase):
    """

    """
    def test_start_view(self):
        """
        Test get root
        :return:
        """
        from OrcView.Driver.Web.Window.WindowView import WindowView
        OrcTest.test_print_begin()

        _view = QApplication(sys.argv)

        tp = WindowView()
        tp.show()

        _view.exec_()

        OrcTest.test_print_end()

    def test_widget_def(self):
        """
        Test get root
        :return:
        """
        from OrcView.Driver.Web.Widget.WidgetDefView import WidgetDefView

        OrcTest.test_print_begin()

        _view = QApplication(sys.argv)

        tp = WidgetDefView()
        tp.show()

        _view.exec_()

        OrcTest.test_print_end()

    def test_view_data(self):
        """
        Test get root
        :return:
        """
        from OrcView.Batch.init_env import DataView

        OrcTest.test_print_begin()

        OrcTest.display_widget(DataView)

        OrcTest.test_print_end()