import unittest

from OrcLib.LibTest import OrcTest
from OrcLib.LibNet import OrcHttpResource


class TestDict(unittest.TestCase):

    def test_http_res_01(self):
        """
        test get dict
        :return:
        """
        OrcTest.test_print_begin()

        _obj = OrcHttpResource('BatchDef')
        _res = _obj.get()

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_http_res_with_id_01(self):
        """
        test get dict
        :return:
        """
        OrcTest.test_print_begin()

        _obj = OrcHttpResource('BatchDef')
        _obj.set_id(1000000001)
        _res = _obj.get()

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()