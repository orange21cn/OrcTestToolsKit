# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibException import OrcApiModelFailException
from RunDefMod import RunDefMod


class RunDefBus(object):

    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog("api.run.bus.run_def")
        self.__model_run_def = RunDefMod()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_run_def.usr_add(p_data)
        except Exception:
            self.__logger.error("Add run error, input: %s" % p_data)
            raise OrcApiModelFailException

        return result

    def bus_list_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        try:
            self.__model_run_def.usr_delete(p_list)
        except Exception:
            self.__logger.error("Add batch error, input: %s" % p_list)
            raise OrcApiModelFailException

        return True

    def bus_list_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_run_def.usr_search(p_cond)
        except Exception:
            self.__logger.error("Add batch error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result
