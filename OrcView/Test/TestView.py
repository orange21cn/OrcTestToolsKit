import unittest

from OrcLib.LibTest import OrcTest


class TestView(unittest.TestCase):

    def test_case(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Batch.BatchDefView import BatchDefView

        OrcTest.display_widget(BatchDefView)

        OrcTest.test_print_end()
