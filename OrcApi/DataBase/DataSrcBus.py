# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibApi import OrcBus

from DataSrcMod import DataSrcMod


class DataSrcBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, 'DataSrc', DataSrcMod)
