# coding=utf-8
import unittest
from OrcLib.LibTest import OrcTest
from OrcApi.Run.RunCore import RunCore


class TestModel(unittest.TestCase):

    def test_add_01(self):
        """
        增加测试集目录
        :return:
        """
        OrcTest.test_print_begin()

        from OrcLib import get_config

        _configer = get_config()

        _home = _configer.get_option("DEFAULT", "root")
        _file = "%s/run_home/BATCH_1000000001/20161028154127/default.res" % _home
        _model = RunCore()

        _model.load_list(_file)

        OrcTest.test_print_result(_model.list)

        OrcTest.test_print_end()

    def test_run_data_01(self):
        """
        增加测试集目录
        :return:
        """
        OrcTest.test_print_begin()

        from OrcApi.Run.RunData import RunData
        from OrcLib.LibCmd import OrcRecordCmd

        obj = RunData()
        obj.load_list('/Users/zhaojingping/PycharmProjects/AuxiTools/test/OrcTestToolsKit/run_home/CASE_200000008/2017071201/default.res')

        cmd = OrcRecordCmd(dict(desc="", flag="10", id="240000029", pid="", run_det_type="WEB", status="PASS"))
        obj.update_status(cmd)

        obj.update_list('/Users/zhaojingping/PycharmProjects/AuxiTools/test/OrcTestToolsKit/run_home/CASE_200000008/2017071201/default_01.res')

        # OrcTest.test_print_result(_model.list)

        OrcTest.test_print_end()
