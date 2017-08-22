import unittest

from OrcLib.LibTest import OrcTest


class TestData(unittest.TestCase):

    def test_data_sql(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcLibFrame.LibData import OrcDataClient

        obj = OrcDataClient()

        print obj.get_data('PRE', 'CASE', '200000022', '20170809100255')

        OrcTest.test_print_end()