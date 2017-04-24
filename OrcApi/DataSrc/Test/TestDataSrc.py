import unittest

from OrcLib.LibTest import OrcTest
from OrcLib.LibNet import OrcResource


class TestDataSrc(unittest.TestCase):

    def test_search(self):

        OrcTest.test_print_begin()

        test = OrcResource("DataSrc")

        OrcTest.test_print_result(test.get(path='13'))
        OrcTest.test_print_result(test.get(parameter=dict()))

        OrcTest.test_print_end()

    def test_add(self):

        OrcTest.test_print_begin()

        test = OrcResource("DataSrc")

        OrcTest.test_print_result(test.get(parameter=dict()))
        OrcTest.test_print_result(test.post(parameter=dict(name='test', desc='test', db_file='ccc')))
        OrcTest.test_print_result(test.get(parameter=dict()))

        OrcTest.test_print_end()

    def test_delete(self):

        OrcTest.test_print_begin()

        test = OrcResource("DataSrc")

        OrcTest.test_print_result(test.delete(parameter=['14', '15']))

        OrcTest.test_print_end()

    def test_execute(self):

        OrcTest.test_print_begin()

        test = OrcResource("DataSrc")

        OrcTest.test_print_result(test.post(path=13, parameter=dict(SQL='select * from tab_item')))

        OrcTest.test_print_end()
