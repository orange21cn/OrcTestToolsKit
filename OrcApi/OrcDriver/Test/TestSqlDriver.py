import unittest

from OrcLib import init_log
from OrcLib.LibTest import OrcTest
from OrcLib.LibNet import OrcResource

init_log('run')


class TestDataSrc(unittest.TestCase):

    def test_search(self):

        OrcTest.test_print_begin()

        from OrcApi.OrcDriver.SQL.SqlDriver import SqlDriver

        test = SqlDriver()

        OrcTest.test_print_result(test.execute(dict(DATA_SRC='1.PRE', SQL='select * from tab_item;')))

        OrcTest.test_print_end()