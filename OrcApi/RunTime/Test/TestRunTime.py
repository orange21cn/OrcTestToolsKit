import unittest

from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibTest import OrcTest


class TestTab(unittest.TestCase):

    def test_list_add(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        run_time = OrcHttpResource("RunTime")

        data = dict(data_flag="env",
                    data_index=1,
                    data_value="3")
        result = run_time.post(data)

        OrcTest.test_print_result(result)

        OrcTest.test_print_end()

    def test_list_search(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        run_time = OrcHttpResource("RunTime")

        result = run_time.get()

        OrcTest.test_print_result(result)

        OrcTest.test_print_end()

    def test_list_delete(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        run_time = OrcHttpResource("RunTime")

        data = [1]
        result = run_time.delete(data)

        OrcTest.test_print_result(result)

        OrcTest.test_print_end()

    def test_update(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        run_time = OrcHttpResource("RunTime")

        run_time.set_path(2)
        result = run_time.put(dict(data_value=10))

        OrcTest.test_print_result(result)

        OrcTest.test_print_end()

    def test_search(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        run_time = OrcHttpResource("RunTime")

        run_time.set_path(2)
        result = run_time.get()

        OrcTest.test_print_result(result)

        OrcTest.test_print_end()

    def test_delete(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        run_time = OrcHttpResource("RunTime")

        run_time.set_path(1)
        result = run_time.delete()

        OrcTest.test_print_result(result)

        OrcTest.test_print_end()
