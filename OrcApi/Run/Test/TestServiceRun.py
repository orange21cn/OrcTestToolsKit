import unittest

from OrcLib.LibTest import OrcTest
from OrcApi.Run.RunDefMod import RunCore


class TestService(unittest.TestCase):

    def test_get_case_list(self):
        """
        Get page usl
        :return:
        """
        OrcTest.test_print_begin()

        _service = RunCore()
        _service.search_list("CASE", 2000000001)
        _service.save_list("./ccc.xml")

        OrcTest.test_print_end()

    def test_get_batch_list(self):
        """
        Get page usl
        :return:
        """
        OrcTest.test_print_begin()

        _service = RunCore()
        _service.search_list("batch", 1000000008)
        _service.save_list("./abc.xml")

        OrcTest.test_print_end()