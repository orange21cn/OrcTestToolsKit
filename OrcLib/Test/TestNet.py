import unittest
from OrcLib.LibTest import OrcTest
from OrcLib import init_log
from OrcLib.LibNet import OrcParameter


class TestOrcParameter(unittest.TestCase):

    def test_send_para(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        init_log()

        _para_01 = OrcParameter().send_para("abc")
        OrcTest.test_print_result("Parameter para_01 is: %s, type is %s" % (_para_01, type(_para_01)))

        _para_02 = OrcParameter().send_para(["abc", "def"])
        OrcTest.test_print_result("Parameter para_02 is: %s, type is %s" % (_para_02, type(_para_02)))

        _para_03 = OrcParameter().send_para(None)
        OrcTest.test_print_result("Parameter para_03 is: %s, type is %s" % (_para_03, type(_para_03)))

        _para_04 = OrcParameter().send_para(120)
        OrcTest.test_print_result("Parameter para_04 is: %s, type is %s" % (_para_04, type(_para_04)))

        OrcTest.test_print_end()

    def test_save_pic(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        from OrcLib.LibNet import OrcHttpService

        service = OrcHttpService("Driver")
        service.save_pic("abc.png")

        OrcTest.test_print_end()