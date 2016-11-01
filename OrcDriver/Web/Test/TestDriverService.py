import unittest

from OrcDriver.Web.WebObject import ObjectMag
from OrcLib.LibTest import OrcTest
from OrcDriver.Web.WebSocketService import WebSocketService


class TestModel(unittest.TestCase):

    def test_open_page(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _service = WebSocketService()
        _res = _service.usr_search()

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()