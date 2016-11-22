# coding=utf-8
import sys
import unittest

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

        pass

        OrcTest.test_print_end()


class TestView(unittest.TestCase):
    """

    """
    def test_run_def(self):
        """
        Test get root
        :return:
        """
        from OrcView.Run.ReportMain import ViewReportMain
        OrcTest.test_print_begin()

        _view = QApplication(sys.argv)

        tp = ViewReportMain()
        tp.show()

        _view.exec_()

        OrcTest.test_print_end()
