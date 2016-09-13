import unittest

from OrcView.Lib.LibView import operate_to_str
from OrcLib.LibTest import OrcTest


class TestModel(unittest.TestCase):

    def test_open_page(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        print operate_to_str({'OBJECT': '3000000001', 'OPERATE': u'INPUT', 'TYPE': u'PAGE'})

        OrcTest.test_print_end()
