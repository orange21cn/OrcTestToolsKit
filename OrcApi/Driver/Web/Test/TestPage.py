import traceback
import unittest

from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibNet import orc_invoke
from OrcLib.LibTest import OrcTest


class TestApi(unittest.TestCase):

    def test_usr_get_url(self):
        """
        :return:
        """
        OrcTest.test_print_begin()

        _para = {'page_id': '120100000000003', "page_env": "TEST"}
        _url = 'http://localhost:5000/Page/usr_get_url'

        try:
            result = orc_invoke(_url, _para)
            OrcTest.test_print_result(result, 'result')
        except OrcPostFailedException:
            traceback.print_exc()

        OrcTest.test_print_end()
