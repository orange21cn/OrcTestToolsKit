# coding=utf-8


class Test01:

    def __init__(self):
        self.aValue = "TEST_01"
        self.bValue = "TEST_02"

    def func_01(self):
        print self.aValue

    def func_02(self):
        print self.bValue


def ttt(abc):
    _a = abc()
    b = _a.func_01
    c = _a.func_02

    b()
    c()


ttt(Test01)
