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

    def test_add(self):

        OrcTest.test_print_begin()

        pass

        OrcTest.test_print_end()
