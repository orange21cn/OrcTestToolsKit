# coding=utf-8
from OrcLib.LibApi import OrcBus

from DictMod import DictMod


class DictBus(OrcBus):
    """
    Dict list
    """
    def __init__(self):

        OrcBus.__init__(self, "dict", DictMod)
