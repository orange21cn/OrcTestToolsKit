# coding=utf-8
import unittest

from OrcApi.Case.CaseDefMod import CaseDefMod
from OrcLib.LibNet import OrcResource

from OrcLib.LibTest import OrcTest


class TestTab(unittest.TestCase):

    def test_get_root(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        pass

        OrcTest.test_print_end()


class TestCaseDetBus(unittest.TestCase):

    def test_bus_det_up(self):
        """
        测试上移
        :return:
        """
        OrcTest.test_print_begin()

        from OrcApi.Case.StepBus import StepDetBus

        bus = StepDetBus()

        print bus.bus_up(2300000003)

        OrcTest.test_print_end()

    def test_bus_det_down(self):
        """
        测试下移
        :return:
        """
        OrcTest.test_print_begin()

        from OrcApi.Case.StepBus import StepDetBus

        bus = StepDetBus()

        print bus.bus_down(2300000003)

        OrcTest.test_print_end()

    def test_api_det_up(self):
        """
        测试上移
        :return:
        """
        OrcTest.test_print_begin()

        res = OrcResource("StepDet")

        OrcTest.test_print_result(res.post(path=2300000003, parameter=dict(cmd="up")))

        OrcTest.test_print_end()

    def test_api_det_down(self):
        """
        测试上移
        :return:
        """
        OrcTest.test_print_begin()

        res = OrcResource("StepDet")

        OrcTest.test_print_result(res.post(path=2300000003, parameter=dict(cmd="down")))

        OrcTest.test_print_end()