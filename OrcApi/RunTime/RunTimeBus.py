# coding=utf-8
from OrcLib.LibNet import OrcLog
from OrcLib.LibException import OrcApiModelFailException

from RunTimeMod import RunTimeMod


class RunTimeBus(object):

    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog("api.run_time.bus")
        self.__model_run_time = RunTimeMod()

    def bus_list_add(self, p_cond):
        """
        新增
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_run_time.usr_add(p_cond)
        except Exception:
            self.__logger.error("Add run_time error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_list_delete(self, p_list):
        """
        删除 list, 调用单个删除函数
        :param p_list:
        :return:
        """
        try:
            for _id in p_list:
                self.bus_delete(_id)
        except Exception:
            self.__logger.error("Delete run_time error, input: %s" % p_list)
            raise OrcApiModelFailException

        return True

    def bus_list_search(self, p_cond):
        """
        查询 list
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_run_time.usr_search(p_cond)
        except Exception:
            self.__logger.error("Search run_time error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_update(self, p_id, p_cond):
        """
        更新一条
        :param p_id:
        :param p_cond:
        :return:
        """
        cond = dict(id=p_id)
        cond.update(p_cond)

        try:
            self.__model_run_time.usr_update(cond)
        except Exception:
            self.__logger.error("Update run_time error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return True

    def bus_delete(self, p_id):
        """
        删除一条
        :param p_id:
        :return:
        """
        try:
            self.__model_run_time.usr_delete(p_id)
        except Exception:
            self.__logger.error("Delete run_time error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询一条
        :param p_id:
        :return:
        """
        try:
            result = self.__model_run_time.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Search run_time error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result
