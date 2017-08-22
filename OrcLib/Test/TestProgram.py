import unittest
from OrcLib.LibTest import OrcTest


class TestDict(unittest.TestCase):

    def test_ordered_dict_01(self):
        """
        Test get exist option
        """
        OrcTest.test_print_begin()

        from OrcLib.LibProgram import OrcFactory

        _data = OrcFactory.create_ordered_dict()
        _data.append("a", 1)
        _data.append("b", 2)
        _data.append("c", 3)
        _data.append("d", 4)
        _data.append("e", 5)
        _data.append("f", 6)

        print _data.dict()

        for _key, _value in _data.items():
            print _key, _value

        _data.delete(3)

        for _key, _value in _data.items():
            print _key, _value

        OrcTest.test_print_end()
