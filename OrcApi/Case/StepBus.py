# coding=utf-8
from OrcLib.LibApi import OrcBus
from OrcLib.LibException import OrcApiModelFailException

from StepDefMod import StepDefMod
from StepDetMod import StepDetMod
from ItemBus import ItemBus


class StepDefBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "step_def", StepDefMod)

        self.__bus_step_det = StepDetBus()

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
            self._model.usr_delete(p_id)

        except Exception:
            self._logger.error("Delete step error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True


class StepDetBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "step_det", StepDetMod)

        self.__bus_item = ItemBus()

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
            print "@@@@@", p_id
            # delete step_det
            self._model.usr_delete(p_id)

        except Exception:
            self._logger.error("Delete step error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True

    def bus_up(self, p_id):
        """
        步骤项上移
        :param p_id:
        :return:
        """
        # 查询步骤信息
        item_info = self._model.usr_search(dict(id=p_id))

        if not item_info:
            return False

        item_info = item_info[0]
        item_no = item_info.item_no
        pre_item_no = int(item_no) - 1

        # 查找最小值
        items = self._model.usr_search(dict(step_id=item_info.step_id))
        min_no = min([item.item_no for item in items])

        if item_no == min_no:
            return False, u"已经是第一个步骤"

        # 查找上一个步骤
        pre_item = self._model.usr_search(
            dict(step_id=item_info.step_id, item_no=pre_item_no))

        # 互换位置
        if pre_item:
            pre_item = pre_item[0]
            self._model.usr_update(dict(id=pre_item.id, item_no=item_no))

        try:
            self._model.usr_update(dict(id=item_info.id, item_no=pre_item_no))
        except AttributeError:
            return False

        return True

    def bus_down(self, p_id):
        """
        步骤项上移
        :param p_id:
        :return:
        """
        # 查询步骤信息
        item_info = self._model.usr_search(dict(id=p_id))

        if not item_info:
            return False

        item_info = item_info[0]
        item_no = item_info.item_no
        next_item_no = int(item_no) + 1

        # 查找最大值
        items = self._model.usr_search(dict(step_id=item_info.step_id))
        max_no = max([item.item_no for item in items])

        if item_no == max_no:
            return False, u"已经是最后一个步骤"

        # 查找下一个步骤
        next_item = self._model.usr_search(
            dict(step_id=item_info.step_id, item_no=next_item_no))

        # 互换位置
        if next_item:
            next_item = next_item[0]
            self._model.usr_update(dict(id=next_item.id, item_no=item_no))

        try:
            self._model.usr_update(dict(id=item_info.id, item_no=next_item_no))
        except AttributeError:
            return False

        return True
