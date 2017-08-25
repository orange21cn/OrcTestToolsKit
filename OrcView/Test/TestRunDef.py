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
        from OrcView.OrcRun.RunDef import ViewRunDef
        OrcTest.test_print_begin()

        _view = QApplication(sys.argv)

        tp = ViewRunDef()
        tp.show()

        _view.exec_()

        OrcTest.test_print_end()

    def test_run_det(self):
        """
        Test get root
        :return:
        """
        from OrcView.OrcRun.RunDet import ViewRunDet
        from OrcLib import get_config

        OrcTest.test_print_begin()

        _view = QApplication(sys.argv)

        tp = ViewRunDet()

        _configer = get_config()
        _home = _configer.get_option("DEFAULT", "root")
        _file = "%s/run_home/BATCH_1000000001/20161028160724/default.res" % _home
        tp.mod_refresh(_file)

        tp.show()

        _view.exec_()

        OrcTest.test_print_end()

    def test_run_main(self):
        """
        Test get root
        :return:
        """
        from OrcView.Run.RunMain import ViewRunMain

        OrcTest.test_print_begin()

        _view = QApplication(sys.argv)

        tp = ViewRunMain()

        tp.show()

        _view.exec_()

        OrcTest.test_print_end()
