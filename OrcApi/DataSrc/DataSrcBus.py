# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibApi import OrcBus

from DataSrcMod import DataSrcMod


class DataSrcBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, 'DataSrc', DataSrcMod)

    def bus_post(self, p_id, p_cmd):
        """
        执行 sql
        :param p_id:
        :param p_cmd:
        :return:
        """
        try:
            return self._model.usr_execute(p_id, p_cmd)
        except Exception:
            pass
