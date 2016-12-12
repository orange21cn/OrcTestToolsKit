import traceback
import unittest

from OrcLib.LibTest import OrcTest
from OrcLib.LibException import OrcPostFailedException


class TestModel(unittest.TestCase):

    def test_usr_search(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        pass

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_usr_search(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        i_para = {'id': '1003'}
        i_url = 'http://127.0.0.1:5000/PageDet/usr_search'

        pass

        OrcTest.test_print_end()
