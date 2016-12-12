# coding=utf-8
from OrcLib import init_log
from OrcLib.LibLog import OrcLog
from OrcLib.LibException import OrcApiModelFailException

from StepDefMod import StepDefMod
from StepDetMod import StepDetMod
from ItemBus import ItemBus


class StepDefBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.step.bus.step_def")
        self.__model_step_def = StepDefMod()
        self.__bus_step_det = StepDetBus()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_step_def.usr_add(p_data)
        except Exception:
            self.__logger.error("Add step error, input: %s" % p_data)
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
            self.__logger.error("Delete step error, input: %s" % p_list)
            raise OrcApiModelFailException

        return True

    def bus_list_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_step_def.usr_search(p_cond)
        except Exception:
            self.__logger.error("Search step error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_delete(self, p_id):
        """
        删除单一步骤
        :param p_id:
        :return:
        """
        try:

            # step_def
            step = self.bus_search(p_id)

            # step_det
            step_det = self.__bus_step_det.bus_list_search(dict(step_id=step.id))
            step_det_ids = [item.id for item in step_det]

            # delete step_det
            self.__bus_step_det.bus_list_delete(step_det_ids)

            # delete step_def
            self.__model_step_def.usr_delete(p_id)

        except Exception:
            self.__logger.error("Delete step error, input: %s" % p_id)
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
            self.__model_step_def.usr_update(cond)
        except Exception:
            self.__logger.error("Update step error, input: %s" % cond)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询单一步骤
        :param p_id:
        :return:
        """
        try:
            result = self.__model_step_def.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Search step error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result


class StepDetBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.step.bus.step_def")
        self.__model_step_det = StepDetMod()
        self.__bus_item = ItemBus()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_step_det.usr_add(p_data)
        except Exception:
            self.__logger.error("Add step error, input: %s" % p_data)
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
            self.__logger.error("Delete step error, input: %s" % p_list)
            raise OrcApiModelFailException

        return True

    def bus_list_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """

        try:
            result = self.__model_step_det.usr_search(p_cond)
        except Exception:
            self.__logger.error("Search step error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_delete(self, p_id):
        """
        删除单一 item
        :param p_id:
        :return:
        """
        try:
            # step_det
            step_det = self.bus_search(p_id)

            # item
            items = self.__bus_item.bus_list_search(dict(id=step_det.item_id))

            item_ids = [item.id for item in items]

            # delete item
            self.__bus_item.bus_list_delete(item_ids)

            # delete step_det
            self.__model_step_det.usr_delete(p_id)

        except Exception:
            self.__logger.error("Delete step error, input: %s" % p_id)
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
            self.__model_step_det.usr_update(cond)
        except Exception:
            self.__logger.error("Update step error, input: %s" % cond)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询单一条目
        :param p_id:
        :return:
        """
        try:
            result = self.__model_step_det.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Search step error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result
