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

    def test_creator(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Batch.BatchDefView import BatchDefSelector

        OrcTest.display_widget(BatchDefSelector)

        OrcTest.test_print_end()

    def test_add(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        def test(a):
            print a

        import sys
        from OrcView.Case.Case.CaseSelector import CaseSelector
        from OrcView.Batch.BatchSelector import BatchSelector
        from OrcView.Lib.LibAdd import BaseAdder
        from OrcView.Driver.Web.Page.PageSelector import PageSelector
        from PySide.QtGui import QApplication

        main = QApplication(sys.argv)

        # _view = Add()
        # _view.show()

        # _view.sig_submit.connect(test)
        # _view.sig_clicked.connect(test)

        print "======>", PageSelector.static_get_data()

        main.exec_()

        OrcTest.test_print_end()