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

