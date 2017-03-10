import unittest

from OrcView.Lib.LibView import operate_to_str
from OrcLib.LibTest import OrcTest


class TestModel(unittest.TestCase):

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