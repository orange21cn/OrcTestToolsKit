
import unittest

from OrcLib.LibTest import OrcTest


class TestView(unittest.TestCase):

    def test_server(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Main.Tools.Server import Server

        OrcTest.display_widget(Server)

        OrcTest.test_print_end()
