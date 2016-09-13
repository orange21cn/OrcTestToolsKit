import unittest

from OrcDriver.Web.WebObject import ObjectMag
from OrcLib.LibTest import OrcTest
from OrcDriver.Web.service import DriverService


class TestService(unittest.TestCase):

    def test_page_get_url(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _service = DriverService()
        _res = _service.page_get_url()

        OrcTest.test_print_result(_res)

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
