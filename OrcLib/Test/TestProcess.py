import unittest
from OrcLib.LibTest import OrcTest
from OrcLib import init_log

import OrcLib.LibProcess

init_log()


class TestLibProcess(unittest.TestCase):

    def test_case(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        print OrcLib.LibProcess.get_case_mark(2000000002)

        OrcTest.test_print_end()

    def test_step(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        print OrcLib.LibProcess.get_step_mark(2200000016)

        OrcTest.test_print_end()

    def test_item(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        print OrcLib.LibProcess.get_item_mark(2400000015)

        OrcTest.test_print_end()

    def test_batch(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        print OrcLib.LibProcess.get_batch_mark(1000000024)

        OrcTest.test_print_end()

    def test_page_def(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        print OrcLib.LibProcess.get_page_def_mark(3000000001)

        OrcTest.test_print_end()

    def test_page_det(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        print OrcLib.LibProcess.get_page_det_mark(3100000001)

        OrcTest.test_print_end()

    def test_widget_def(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        print OrcLib.LibProcess.get_widget_mark(3300000004)

        OrcTest.test_print_end()
