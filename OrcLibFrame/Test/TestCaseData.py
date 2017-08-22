import unittest

from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibTest import OrcTest


class TestTab(unittest.TestCase):

    def test_case(self):
        """
        Test get root
        :return:
        """
        def print_tree(p_node, p_level=0):

            print "    " * p_level, p_node['content']['id'], obj.raw_data(p_node['content']['id'])

            for i in p_node['children']:
                print_tree(i, p_level + 1)

        OrcTest.test_print_begin()

        from OrcLibFrame.LibCaseData import CaseData

        obj = CaseData()

        obj.load_case('200000008')
        print obj.get_items()

        OrcTest.test_print_end()

    def test_step(self):
        """
        Test get root
        :return:
        """
        def print_tree(p_node, p_level=0):

            print "    " * p_level, p_node['content']['id'], obj.raw_data(p_node['content']['id'])

            for i in p_node['children']:
                print_tree(i, p_level + 1)

        OrcTest.test_print_begin()

        from OrcLibFrame.LibCaseData import CaseData

        obj = CaseData()

        obj.load_step('220000011')
        for i in obj.get_items():
            print i


        OrcTest.test_print_end()