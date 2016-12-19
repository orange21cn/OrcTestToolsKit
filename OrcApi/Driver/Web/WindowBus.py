# coding=utf-8
from OrcLib.LibApi import OrcBus

from WindowDefMod import WindowDefMod


class WindowDefBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "window_def", WindowDefMod)
