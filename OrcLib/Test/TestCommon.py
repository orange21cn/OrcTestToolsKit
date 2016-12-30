import unittest
from OrcLib.LibTest import OrcTest
from OrcLib.LibCommon import OrcCovert


class TestCovert(unittest.TestCase):

    def test_time2char_01(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        import datetime

        _lib = OrcCovert()

        _res = _lib.time2str(datetime.datetime.now())

        OrcTest.test_print_result(_res)
        OrcTest.test_print_end()

    def test_time2char_02(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        _lib = OrcCovert()

        _res = _lib.time2str(1)

        OrcTest.test_print_result(_res)
        OrcTest.test_print_end()

    def test_char2time_01(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        _lib = OrcCovert()
        _res = _lib.str2time("2016-09-19 17:32:47")

        OrcTest.test_print_result(_res)
        OrcTest.test_print_end()
