import unittest

from OrcLib.LibTest import OrcTest
from OrcDriver.Web.WebSocketServer import DriverSelenium


class TestWidget(unittest.TestCase):

    def test_widget_definition_01(self):
        """
        Test get widget definition
        :return:
        """
        OrcTest.test_print_begin()

        _widget = OrcWidget(None, 3200000008)

        for i in _widget._def:
            OrcTest.test_print_result(i["DEF"].id)
            for j in i["DET"]:
                OrcTest.test_print_result(j.id)

        OrcTest.test_print_end()
