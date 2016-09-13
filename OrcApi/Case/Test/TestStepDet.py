import unittest

from OrcCase.StepDetModel import StepDetHandle

from OrcLib import OrcTest


class TestTab(unittest.TestCase):

    def test_get_root(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        test = StepDetHandle()
        ttt = test.usr_search({'id': u'1010'})
        OrcTest.test_print_result(ttt[0].to_json())

        OrcTest.test_print_end()
