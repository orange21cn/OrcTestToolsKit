import unittest

from OrcData.DataModel import DataHandle

from OrcLib import OrcTest


class TestData(unittest.TestCase):

    def test_get_data(self):

        OrcTest.test_print_begin()

        test = DataHandle()
        _res = test.usr_search()
        for i in _res:
            OrcTest.test_print_result(i.to_json())

        OrcTest.test_print_end()

    def test_add(self):

        OrcTest.test_print_begin()

        test = DataHandle()
        _res = test.usr_add()

        for i in _res:
            OrcTest.test_print_result(_res[i])

        OrcTest.test_print_end()
