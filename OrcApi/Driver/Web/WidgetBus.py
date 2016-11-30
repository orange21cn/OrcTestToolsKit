# coding=utf-8
from OrcLib import init_log
from OrcLib.LibLog import OrcLog
from OrcLib.LibException import OrcApiModelFailException

from WidgetDefMod import WidgetDefMod
from WidgetDetMod import WidgetDetMod


class WidgetDefBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.step.bus.step_def")
        self.__model_widget_def = WidgetDefMod()
        self.__bus_widget_det = WidgetDetBus()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_widget_def.usr_add(p_data)
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
            result = self.__model_widget_def.usr_search(p_cond)
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_delete(self, p_id):
        """
        删除单一步骤
        :param p_id:
        :return:
        """
        try:
            self.__model_widget_def.usr_delete(p_id)
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True

    def bus_update(self, p_id, p_cond):
        """
        更新步骤
        :param p_id:
        :param p_cond:
        :return:
        """
        cond = dict(id=p_id).update(p_cond)

        try:
            self.__model_widget_def.usr_update(cond)
        except Exception:
            self.__logger.error("Add case error, input: %s" % cond)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询单一步骤
        :param p_id:
        :return:
        """
        try:
            result = self.__model_widget_def.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result


class WidgetDetBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.step.bus.step_def")
        self.__model_widget_det = WidgetDetMod()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_widget_det.usr_add(p_data)
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
            result = self.__model_widget_det.usr_search(p_cond)
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_delete(self, p_id):
        """
        删除单一 item
        :param p_id:
        :return:
        """
        try:
            self.__model_widget_det.usr_delete(p_id)
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True

    def bus_update(self, p_id, p_cond):
        """
        更新
        :param p_id:
        :param p_cond:
        :return:
        """
        cond = dict(id=p_id).update(p_cond)

        try:
            self.__model_widget_det.usr_update(cond)
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询单一条目
        :param p_id:
        :return:
        """
        try:
            result = self.__model_widget_det.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result
