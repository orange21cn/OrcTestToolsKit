import unittest

from OrcLib import init_log
from OrcLib.LibTest import OrcTest
from OrcLib.LibNet import OrcResource

init_log('run')


class TestDataSrc(unittest.TestCase):

    def test_search(self):

        OrcTest.test_print_begin()

        test = OrcResource("DataSrc")

        OrcTest.test_print_result(test.get(path='1.PRE'))

        OrcTest.test_print_end()

    def test_add(self):

        OrcTest.test_print_begin()

        test = OrcResource("DataSrc")

        OrcTest.test_print_result(test.post(parameter=dict(name='test', desc='test', env='TEST', db_file='ccc')))
        OrcTest.test_print_result(test.get(parameter=dict()))

        OrcTest.test_print_end()

    def test_delete(self):

        OrcTest.test_print_begin()

        test = OrcResource("DataSrc")

        OrcTest.test_print_result(test.delete(parameter=['19']))

        OrcTest.test_print_end()

    def test_update(self):

        OrcTest.test_print_begin()

        test = OrcResource("DataSrc")
        OrcTest.test_print_result(test.put(path=20, parameter=dict(name='test2', env='PRD', desc='test11', db_file='aaa1')))

        OrcTest.test_print_end()

    def test_search_database(self):

        OrcTest.test_print_begin()

        res = OrcResource('DataBase')
        result = res.get(parameter=dict(DATA_SRC='1.PRE', SQL='select * from tab_item;'))

        OrcTest.test_print_result(result)

        OrcTest.test_print_end()
