import traceback
import unittest

from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibTest import OrcTest
from OrcLib.LibNet import OrcHttpResource

from OrcApi.Lib.Dictionory import DictHandle


class TestFunc(unittest.TestCase):

    def test_get_dict_text(self):
        """
        Test get root
        :return:
        """
        OrcTest.test_print_begin()

        test = DictHandle()
        _para = dict(flag="case_type", value="CASE")
        i = test.get_dict_text(_para)
        OrcTest.test_print_result(i)

        OrcTest.test_print_end()


class TestApi(unittest.TestCase):

    def test_get_dict_text(self):

        OrcTest.test_print_begin()

        i_para = dict(flag="case_type", value="CASE")
        i_url = 'http://127.0.0.1:5000/Lib/get_dict_text'

        pass

        OrcTest.test_print_end()


class TestDict(unittest.TestCase):

    def test_api_list_get(self):

        OrcTest.test_print_begin()

        resource = OrcHttpResource("Dict")
        OrcTest.test_print_result(resource.get(dict(id=10001)))

        OrcTest.test_print_end()

    def test_api_list_post(self):

        OrcTest.test_print_begin()

        resource = OrcHttpResource("Dict")
        OrcTest.test_print_result(resource.post(dict(dict_flag="test_dict", dict_order=1)))

        OrcTest.test_print_end()

    def test_api_list_delete(self):

        OrcTest.test_print_begin()

        resource = OrcHttpResource("Dict")
        OrcTest.test_print_result(resource.delete([20001]))

        OrcTest.test_print_end()

    def test_api_update(self):

        OrcTest.test_print_begin()

        resource = OrcHttpResource("Dict")
        resource.set_path(20003)
        OrcTest.test_print_result(resource.put(dict(dict_flag="update")))

        OrcTest.test_print_end()
