import unittest

from OrcLib.LibTest import OrcTest
from OrcView.Case.Case import ViewCaseDefMag
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibViewDef import view_batch_def


class TestDict(unittest.TestCase):

    def test_get_dict_01(self):
        """
        test get dict
        :return:
        """
        def test(p_str):
            print p_str

        OrcTest.test_print_begin()

        import sys

        from PySide.QtGui import QApplication

        main = QApplication(sys.argv)

        _view = ViewAdd(view_batch_def)
        _view.sig_clicked.connect(test)
        _view.show()

        main.exec_()

        OrcTest.test_print_end()