# coding=utf-8
from OrcLib import init_log
from OrcLib.LibLog import OrcLog
from OrcLib.LibException import OrcApiModelFailException
from DataMod import DataMod


class DataBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.data.bus.data")
        self.__model_data = DataMod()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_data.usr_add(p_data)
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_data)
            raise OrcApiModelFailException

        return result

    def bus_list_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        try:
            for _id in p_list:
                self.bus_delete(_id)
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_list)
            raise OrcApiModelFailException

        return True

    def bus_list_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_data.usr_search(p_cond)
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_delete(self, p_id):
        """
        删除一条
        :param p_id:
        :return:
        """
        try:
            self.__model_data.usr_delete(p_id)
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True

    def bus_update(self, p_id, p_cond):
        """
        更新
        :param p_cond:
        :param p_id:
        :return:
        """
        cond = dict(id=p_id)
        cond.update(p_cond)

        try:
            self.__model_data.usr_update(cond)
        except Exception:
            self.__logger.error("Add case error, input: %s" % cond)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_cond):
        """
        查询一条
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_data.usr_update(p_cond)
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result
