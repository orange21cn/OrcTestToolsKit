import unittest

from OrcLib.LibTest import OrcTest
from OrcLibFrame.LibData import OrcDataClient


class TestData(unittest.TestCase):

    def test_data_int(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        obj = OrcDataClient()
        obj.set_env('PRE')

        print obj.get_data('BATCH', '100000008', '20170809104012')

        OrcTest.test_print_end()

    def test_data_sql(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        obj = OrcDataClient()

        print obj.get_data('BATCH', '100000007', '20170809104012')

        OrcTest.test_print_end()

    def test_data_temp(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        obj = OrcDataClient()
        obj.set_env('PRE')

        # random
        print obj.get_data('BATCH', '100000009', '20170809104012')

        # increase
        print obj.get_data('BATCH', '100000009', '20170809104013')

        # date
        print obj.get_data('BATCH', '100000009', '20170809104014')

        # complex
        print obj.get_data('BATCH', '100000009', '20170809104015')

        OrcTest.test_print_end()

    def test_data_cmd(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        from OrcLib.LibCmd import OrcRecordCmd

        obj = OrcDataClient()
        obj.set_env('PRE')

        # item
        cmd = OrcRecordCmd(dict(id=240000018, run_det_type='WEB'))
        print obj.get_cmd_data(cmd, '20170809104012')
        print

        # step
        cmd = OrcRecordCmd(dict(id=240000018, run_det_type='WEB'))
        print obj.get_cmd_data(cmd, '20170809104013')
        print

        # case
        cmd = OrcRecordCmd(dict(id=240000018, run_det_type='WEB'))
        print obj.get_cmd_data(cmd, '20170809104014')
        print

        # case group
        # case
        cmd = OrcRecordCmd(dict(id=240000018, run_det_type='WEB'))
        print obj.get_cmd_data(cmd, '20170809104015')
        print

        # batch

        OrcTest.test_print_end()
