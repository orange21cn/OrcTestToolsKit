# coding=utf-8
from OrcLib.LibApi import OrcBus
from DataMod import DataMod


class DataBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "data", DataMod)
