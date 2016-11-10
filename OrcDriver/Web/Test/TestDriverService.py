import unittest

from OrcDriver.Web.WebDriver import WebDriverService
from OrcLib.LibTest import OrcTest


class TestModel(unittest.TestCase):

    def test_open_page(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _service = WebDriverService()
        _res = _service.usr_search()

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()