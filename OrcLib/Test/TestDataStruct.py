import unittest
from OrcLib.LibTest import OrcTest
from OrcLib.LibDataStruct import ListTree


class TestListTree(unittest.TestCase):

    def test_list_2_tree(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        _list = [
            dict(id=101, pid=None, data=1),
            dict(id=102, pid=101, data=1),
            dict(id=103, pid=102, data=1),
            dict(id=104, pid=101, data=1),
            dict(id=105, pid=104, data=1),
            dict(id=106, pid=104, data=1),
        ]

        _model = ListTree(data_list=_list)

        OrcTest.test_print_result(_model.tree)

        OrcTest.test_print_end()

    def test_tree_2_list(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        _list = {'content': {'data': 1, 'pid': None, 'id': 101},
                 'children': [
                     {'content': {'data': 1, 'pid': 101, 'id': 102},
                      'children': [
                          {'content': {'data': 1, 'pid': 102, 'id': 103},
                           'children': []}]},
                     {'content': {'data': 1, 'pid': 101, 'id': 104},
                      'children': [
                          {'content': {'data': 1, 'pid': 104, 'id': 105},
                           'children': []},
                          {'content': {'data': 1, 'pid': 104, 'id': 106},
                           'children': []}]}]}

        _model = ListTree(data_tree=_list)

        OrcTest.test_print_result(_model.list)

        OrcTest.test_print_end()

    def test_steps(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        _list = {'content': {'data': 1, 'pid': None, 'id': 101},
                 'children': [
                     {'content': {'data': 1, 'pid': 101, 'id': 102},
                      'children': [
                          {'content': {'data': 1, 'pid': 102, 'id': 103},
                           'children': []}]},
                     {'content': {'data': 1, 'pid': 101, 'id': 104},
                      'children': [
                          {'content': {'data': 1, 'pid': 104, 'id': 105},
                           'children': []},
                          {'content': {'data': 1, 'pid': 104, 'id': 106},
                           'children': []}]}]}

        _model = ListTree(data_tree=_list)

        for i in _model.steps():
            print i

        OrcTest.test_print_end()

    def test_get_child_tree(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        _list = {'content': {'data': 1, 'pid': None, 'id': 101},
                 'children': [
                     {'content': {'data': 1, 'pid': 101, 'id': 102},
                      'children': [
                          {'content': {'data': 1, 'pid': 102, 'id': 103},
                           'children': []}]},
                     {'content': {'data': 1, 'pid': 101, 'id': 104},
                      'children': [
                          {'content': {'data': 1, 'pid': 104, 'id': 105},
                           'children': []},
                          {'content': {'data': 1, 'pid': 104, 'id': 106},
                           'children': []}]}]}

        _model = ListTree()
        _model.load_tree(_list)

        print _model.get_children_tree(106)

        print "----"

        print _model.get_children_list(106)

        OrcTest.test_print_end()

    def test_get_path(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        _list = {'content': {'data': 1, 'pid': None, 'id': 101},
                 'children': [
                     {'content': {'data': 1, 'pid': 101, 'id': 102},
                      'children': [
                          {'content': {'data': 1, 'pid': 102, 'id': 103},
                           'children': []}]},
                     {'content': {'data': 1, 'pid': 101, 'id': 104},
                      'children': [
                          {'content': {'data': 1, 'pid': 104, 'id': 105},
                           'children': []},
                          {'content': {'data': 1, 'pid': 104, 'id': 106},
                           'children': []}]}]}

        _model = ListTree()
        _model.load_tree(_list)

        print _model.get_path(101)
        print _model.get_path(102)
        print _model.get_path(103)
        print _model.get_path(104)
        print _model.get_path(105)
        print _model.get_path(106)

        OrcTest.test_print_end()
