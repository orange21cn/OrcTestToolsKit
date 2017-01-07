import unittest

from OrcView.Lib.LibView import operate_to_str
from OrcLib.LibTest import OrcTest


class TestModel(unittest.TestCase):

    def test_open_page(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        print operate_to_str({'OBJECT': '3000000001', 'OPERATE': u'INPUT', 'TYPE': u'PAGE'})

        OrcTest.test_print_end()

    def test_pagination(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        # User interface
        import sys
        from OrcView.Lib.LibView import OrcPagination
        from PySide.QtGui import QApplication

        view = QApplication(sys.argv)

        def test(flg):
            print flg

        tp = OrcPagination()
        tp.sig_page.connect(test)
        tp.show()

        view.exec_()

        OrcTest.test_print_end()
