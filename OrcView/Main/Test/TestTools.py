
import unittest

from OrcLib.LibTest import OrcTest


class TestView(unittest.TestCase):

    def test_resource(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Main.Tools.Server import ServerResource

        OrcTest.display_widget(ServerResource)

        OrcTest.test_print_end()

    def test_run(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Main.Tools.Server import ServerRun

        OrcTest.display_widget(ServerRun)

        OrcTest.test_print_end()

    def test_report(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Main.Tools.Server import ServerReport

        OrcTest.display_widget(ServerReport)

        OrcTest.test_print_end()


class TestRun(unittest.TestCase):

    def test_run_env(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Main.Tools.Run import RunEnv

        OrcTest.display_widget(RunEnv)

        OrcTest.test_print_end()

    def test_run_browser(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcView.Main.Tools.Run import RunBrowser

        OrcTest.display_widget(RunBrowser)

        OrcTest.test_print_end()