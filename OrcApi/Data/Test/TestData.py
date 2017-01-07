import unittest

from OrcLib.LibTest import OrcTest
from OrcLib.LibNet import OrcHttpResource


class TestData(unittest.TestCase):

    def test_get_data(self):

        OrcTest.test_print_begin()

        test = OrcHttpResource("Data")
        result = test.get({"src_type": "CASE", "data_flag": "3300000019", "src_id": "2000000003"})
        OrcTest.test_print_result(result)

        OrcTest.test_print_end()

    def test_model_search(self):

        OrcTest.test_print_begin()

        from OrcApi.Data.DataMod import DataMod

        model = DataMod()
        cond = dict(page=1, number=3, condition=dict())
        print model.usr_search(cond)

        OrcTest.test_print_end()
