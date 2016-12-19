# coding=utf-8
from OrcLib.LibApi import OrcBus

from ItemMod import ItemMod


class ItemBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "item", ItemMod)
