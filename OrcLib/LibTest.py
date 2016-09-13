import sys


class OrcTest:

    def __init__(self):
        pass

    @staticmethod
    def test_print_result(p_result, p_result_name=None):
        if p_result_name is not None:
            print "%s's value is: " % p_result_name
        print p_result

    @staticmethod
    def test_print_end():
        print "<--- Case %s end ----------------------<" % sys._getframe().f_back.f_code.co_name
        print ""

    @staticmethod
    def test_print_begin():
        print ">--- Case %s begin -------------------->" % sys._getframe().f_back.f_code.co_name
