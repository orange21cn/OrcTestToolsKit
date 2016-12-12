# coding=utf-8
from OrcLib import init_log
from OrcLib.LibNet import OrcLog
from OrcLib.LibException import OrcApiModelFailException

from DictMod import DictMod


class DictListBus(object):
    """
    Dict list
    """
    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.lib.bus.dicts")
        self.__model_dict = DictMod()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_dict.mod_add(p_data)
        except Exception:
            self.__logger.error("Add dict error, input: %s" % p_data)
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
                self.__model_dict.mod_delete(_id)
        except Exception:
            self.__logger.error("Delete dict error, input: %s" % p_list)
            raise OrcApiModelFailException

        return True

    def bus_list_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_dict.mod_search(p_cond)
        except Exception:
            self.__logger.error("Search dict error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result


class DictBus(object):
    """
    Dict
    """
    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.lib.bus.dict")
        self.__model_dict = DictMod()

    def bus_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        try:
            result = self.__model_dict.mod_search(p_id)
        except Exception:
            self.__logger.error("Delete dict error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result

    def bus_update(self, p_id, p_cond):
        """
        更新
        :param p_id:
        :param p_cond:
        :return:
        """
        print p_cond
        cond = dict(id=p_id)
        cond.update(p_cond)
        print cond
        try:
            self.__model_dict.mod_update(cond)
        except Exception:
            self.__logger.error("Update dict error, input: %s" % cond)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询
        :param p_id:
        :return:
        """
        try:
            result = self.__model_dict.mod_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Update dict error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result
