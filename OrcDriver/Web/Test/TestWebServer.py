import unittest

from OrcDriver.Web.WebObject import ObjectMag
from OrcLib.LibTest import OrcTest


class TestSelenium(unittest.TestCase):

    def test_open_page(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = ObjectMag()
        _handle.open_page("120100000000003")

        OrcTest.test_print_end()

    def test_get_widget(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _handle = ObjectMag()
        _handle.get_widget("120300000000022")

        OrcTest.test_print_end()
