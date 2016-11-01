import unittest

from OrcDriver.Web.WebSocketServer import DriverSelenium
from OrcDriver.Web.Widget.OrcWidget import OrcWidget
from OrcLib.LibNet import orc_invoke
from OrcLib.LibTest import OrcTest


class TestSelenium(unittest.TestCase):

    def test_open_page(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _data = dict(TYPE="PAGE", BROWSER="FIREFOX", ENV="TESTa", ID="3000000001")
        _url = "http://localhost:5002/WebServer/run"
        _res = orc_invoke(_url, _data)

        OrcTest.test_print_result(_res)
        OrcTest.test_print_end()

    def test_get_widget(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        _data = dict(TYPE="WIDGET", ID="3300000005", OPERATION="CLICK")
        _url = "http://localhost:5002/WebServer/run"
        _res = orc_invoke(_url, _data)

        OrcTest.test_print_result(_res)
        OrcTest.test_print_end()

    def test_widget_definition_02(self):
        """
        Test widget is not exist
        :return:
        """
        OrcTest.test_print_begin()

        _driver = DriverSelenium()

        _para_01 = dict(TYPE="GET_PAGE",
                        PARA=dict(BROWSER="FIREFOX", ENV="TEST",ID="3100000005"),
                        OPERATE=None)
        _driver.__execute(_para_01)

        _para_02 = dict(TYPE="GET_WIDGET",
                        PARA=3200000011,
                        OPERATE=None)
        _driver.__execute(_para_02)

        OrcTest.test_print_end()
