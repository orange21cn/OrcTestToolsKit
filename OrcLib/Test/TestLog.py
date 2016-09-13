import unittest
from OrcLib.LibTest import OrcTest
from OrcLib import init_log
from OrcLib.LibLog import OrcLog


class TestLog(unittest.TestCase):

    def test_log_api(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        init_log()

        _log = OrcLog("api.test01")

        _log.info("This 001!")
        _log.warning("This 002!")
        _log.error("This 003!")
        _log.critical("This 004!")
        _log.debug("This 005!")

        OrcTest.test_print_end()

    def test_log_basic(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        init_log()

        _log = OrcLog("basic.test01")

        _log.info("This 001!")
        _log.warning("This 002!")
        _log.error("This 003!")
        _log.critical("This 004!")
        _log.debug("This 005!")

        OrcTest.test_print_end()

    def test_log_view(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        init_log()

        _log = OrcLog("view.test01")

        _log.info("This 001!")
        _log.warning("This 002!")
        _log.error("This 003!")
        _log.critical("This 004!")
        _log.debug("This 005!")

        OrcTest.test_print_end()