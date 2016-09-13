import unittest
from OrcLib.LibTest import OrcTest
from OrcLib import get_config


class TestConfig(unittest.TestCase):

    def test_get_option_01(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        _cfg = get_config()
        _res = _cfg.get_option("TEST", "OPT_01")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_option_02(self):
        """
        Section is not exists
        """
        OrcTest.test_print_begin()

        _cfg = get_config()
        _res = _cfg.get_option("NOT_EXISTS", "OPT_01")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_option_03(self):
        """
        Option is not exists
        """
        OrcTest.test_print_begin()

        _cfg = get_config()
        _res = _cfg.get_option("TEST", "NOT_EXISTS")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_options_01(self):
        """
        Get exist options
        :return:
        """
        OrcTest.test_print_begin()

        _cfg = get_config()
        _res = _cfg.get_options("TEST")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_options_02(self):
        """
        Sections is not exists
        :return:
        """
        OrcTest.test_print_begin()

        _cfg = get_config()
        _res = _cfg.get_options("NOT_EXISTS")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_set_option_01(self):
        """
        Set option
        :return:
        """
        OrcTest.test_print_begin()

        _cfg = get_config()
        OrcTest.test_print_result(_cfg.get_option("TEST", "OPT_01"))
        _cfg.set_option("TEST", "OPT_01", "opt_01")
        OrcTest.test_print_result(_cfg.get_option("TEST", "OPT_01"))

        OrcTest.test_print_end()

    def test_set_option_02(self):
        """
        Section is not exists
        :return:
        """
        OrcTest.test_print_begin()

        _cfg = get_config()
        OrcTest.test_print_result(_cfg.get_option("TEST", "OPT_01"))
        _cfg.set_option("NOT_EXISTS", "OPT_01", "opt_01")
        OrcTest.test_print_result(_cfg.get_option("TEST", "OPT_01"))

        OrcTest.test_print_end()

    def test_set_option_03(self):
        """
        Option is not exists
        :return:
        """
        OrcTest.test_print_begin()

        _cfg = get_config()
        OrcTest.test_print_result(_cfg.get_option("TEST", "OPT_01"))
        _cfg.set_option("TEST", "NOT_EXISTS", "opt_01")
        OrcTest.test_print_result(_cfg.get_option("TEST", "OPT_01"))

        OrcTest.test_print_end()


class TestConfigFile(unittest.TestCase):

    def test_get_option_01(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        _cfg = get_config("test")
        _res = _cfg.get_option("TEST", "OPT_01")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_get_options_01(self):
        """
        Get exist options
        :return:
        """
        OrcTest.test_print_begin()

        _cfg = get_config("test")
        _res = _cfg.get_options("TEST")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_set_option_01(self):
        """
        Set option
        :return:
        """
        OrcTest.test_print_begin()

        _cfg = get_config("test")
        OrcTest.test_print_result(_cfg.get_option("TEST", "OPT_02"))
        _cfg.set_option("TEST", "OPT_02", "opt_01")
        OrcTest.test_print_result(_cfg.get_option("TEST", "OPT_02"))

        OrcTest.test_print_end()

    def test_get_option_02(self):
        """
        File is not exists
        """
        OrcTest.test_print_begin()

        _cfg = get_config("NOT_EXISTS")
        _res = _cfg.get_option("TEST", "OPT_01")

        OrcTest.test_print_result(_res)

        OrcTest.test_print_end()

    def test_000(self):
        """
        File is not exists
        """
        OrcTest.test_print_begin()

        import os

        _cfg = get_config()
        _cfg.set_option("MAIN", "ROOT", "%s/.." % os.path.dirname(__file__))

        OrcTest.test_print_end()
