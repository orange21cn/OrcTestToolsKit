import traceback
import unittest

from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibTest import OrcTest


class TestApi(unittest.TestCase):

    def test_usr_get_def(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _para = {'id': '120300000000022'}
        _url = 'http://localhost:5000/Widget/usr_get_def'

        pass

        OrcTest.test_print_end()

    def test_usr_get_det(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _para = {'widget_id': '120300000000023'}
        _url = 'http://localhost:5000/Widget/usr_get_det'

        pass

        OrcTest.test_print_end()