import unittest

from OrcLib.LibNet import orc_invoke
from OrcLib.LibTest import OrcTest


class TestSelenium(unittest.TestCase):

    def test_open_page(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _data = dict(TYPE="GET_PAGE",
                     PARA=dict(BROWSER="FIREFOX", ENV="TEST",ID="3100000004"))
        _url = "http://localhost:5002/WebServer/run"
        _res = orc_invoke(_url, _data)

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()
