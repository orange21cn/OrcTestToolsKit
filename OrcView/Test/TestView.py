import unittest

from OrcView.Lib.LibView import operate_to_str
from OrcLib.LibTest import OrcTest


class TestView(unittest.TestCase):

    def test_case(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Case.Case.CaseView import CaseView

        OrcTest.display_widget(CaseView)

        OrcTest.test_print_end()

    def test_case_sel_sig(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Case.Case.CaseView import CaseView

        OrcTest.display_widget(CaseView, 'SINGLE')

        OrcTest.test_print_end()

    def test_case_sel_mul(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Case.Case.CaseView import CaseView

        OrcTest.display_widget(CaseView, 'MULTI')

        OrcTest.test_print_end()

    def test_widget(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.Widget.WidgetDefView import WidgetDefView

        OrcTest.display_widget(WidgetDefView)

        OrcTest.test_print_end()

    def test_widget_sel(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.Widget.WidgetDefView import WidgetDefView

        OrcTest.display_widget(WidgetDefView, 'SINGLE')

        OrcTest.test_print_end()

    def test_page(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.Page.PageDefView import PageDefView

        OrcTest.display_widget(PageDefView)

        OrcTest.test_print_end()

    def test_page_sel(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Driver.Web.Page.PageDefView import PageDefView

        OrcTest.display_widget(PageDefView, 'SINGLE')

        OrcTest.test_print_end()

    def test_data_src(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Data.DataSrc.DataSrcView import DataSrcMain

        OrcTest.display_widget(DataSrcMain)

        OrcTest.test_print_end()

    def test_view_create(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        import sys
        from PySide.QtGui import QApplication
        from OrcView.Lib.LibView import WidgetFactory

        main = QApplication(sys.argv)

        wfc = WidgetFactory()

        _view = wfc.create_widget('DATASRC')
        _view.show()

        main.exec_()

        OrcTest.test_print_end()

    def test_mem_data(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Tools.MemData.RunTimeView import RunTimeDispView

        OrcTest.display_widget(RunTimeDispView)

        OrcTest.test_print_end()

    def test_mem_main(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Tools.MemData.RunMainView import RunMainView

        OrcTest.display_widget(RunMainView)

        OrcTest.test_print_end()

    def test_conf(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Config.ConfView import ConfMain

        OrcTest.display_widget(ConfMain)

        OrcTest.test_print_end()

    def test_debug(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Run.Debug.DebugMain import DebugMain

        OrcTest.display_widget(DebugMain)

        OrcTest.test_print_end()


class TestModel(unittest.TestCase):

    def test_case_02(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Lib.LibView import WidgetFactory

        wfc = WidgetFactory()

        OrcTest.test_print_end()
