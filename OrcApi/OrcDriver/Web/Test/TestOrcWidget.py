import unittest

from OrcLib.LibTest import OrcTest
from OrcDriver.Web.Widget.OrcWidget import OrcWidget


class TestWidget(unittest.TestCase):

    def test_widget_definition_01(self):
        """
        Test get widget definition
        :return:
        """
        OrcTest.test_print_begin()

        _widget = OrcWidget(None, 3300000014)

        for i in _widget._def:

            OrcTest.test_print_result(i["DEF"].id, "id")
            OrcTest.test_print_result(i["DET"], "detail")

            if i["DET"] is not None:
                for j in i["DET"]:
                    OrcTest.test_print_result(j.id, "det_id")

        OrcTest.test_print_end()
