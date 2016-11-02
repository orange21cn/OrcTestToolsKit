import unittest

from OrcDriver.Web.WebSocketServer import WebSocketService
from OrcLib.LibTest import OrcTest


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