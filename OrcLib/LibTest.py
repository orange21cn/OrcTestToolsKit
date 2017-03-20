# coding=utf-8
import sys
from OrcLib import init_log


class OrcTest:

    def __init__(self):
        pass

    @staticmethod
    def test_print_result(p_result, p_result_name=None):
        if p_result_name is not None:
            print "%s's value is: %s" % (p_result_name, p_result)
        else:
            print p_result

    @staticmethod
    def test_print_end():
        print "<--- Case %s end ----------------------<" % sys._getframe().f_back.f_code.co_name
        print ""

    @staticmethod
    def test_print_begin():
        print ">--- Case %s begin -------------------->" % sys._getframe().f_back.f_code.co_name
        # init_log()

    @staticmethod
    def test_print_result(p_result):
        print p_result
        print "status: %s" % p_result.status
        print "message: %s" % p_result.message
        print "data: %s" % p_result.data

    @staticmethod
    def display_widget(p_widget, *args):

        from PySide.QtGui import QApplication

        main = QApplication(sys.argv)

        _view = p_widget(*args)
        _view.show()

        main.exec_()
