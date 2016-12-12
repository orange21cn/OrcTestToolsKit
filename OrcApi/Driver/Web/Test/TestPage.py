import traceback
import unittest

from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibTest import OrcTest


class TestApi(unittest.TestCase):

    def test_usr_get_url(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _para = {'page_id': '120100000000003', "page_env": "TEST"}
        _url = 'http://localhost:5000/Page/usr_get_url'

        pass

        OrcTest.test_print_end()
