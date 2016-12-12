# coding=utf-8
from OrcLib import init_log
from OrcLib.LibLog import OrcLog
from OrcLib.LibException import OrcApiModelFailException

from PageDefMod import PageDefMod
from PageDetMod import PageDetMod


class PageDefBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.step.bus.step_def")
        self.__model_page_def = PageDefMod()
        self.__bus_page_det = PageDetBus()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_page_def.usr_add(p_data)
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
            result = self.__model_page_def.usr_search(p_cond)
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
            # 查找 page_det_list
            page_det_list = self.__bus_page_det.bus_list_search(dict(page_id=p_id))

            # 获取 page_det_id_list
            page_det_id_list = [page_det.id for page_det in page_det_list]

            # 删除 page_dets
            self.__bus_page_det.bus_list_delete(page_det_id_list)

            # 删除 page_def
            self.__model_page_def.usr_delete(p_id)

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
        cond = dict(id=p_id)
        cond.update(p_cond)
        try:
            self.__model_page_def.usr_update(cond)
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
            result = self.__model_page_def.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result


class PageDetBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.step.bus.step_def")
        self.__model_page_det = PageDetMod()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_page_det.usr_add(p_data)
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
            result = self.__model_page_det.usr_search(p_cond)
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
            self.__model_page_det.usr_delete(p_id)
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
        cond = dict(id=p_id)
        cond.update(p_cond)
        try:
            self.__model_page_det.usr_update(cond)
        except Exception:
            self.__logger.error("Add case error, input: %s" % cond)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询单一条目
        :param p_id:
        :return:
        """
        try:
            result = self.__model_page_det.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Add case error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result
