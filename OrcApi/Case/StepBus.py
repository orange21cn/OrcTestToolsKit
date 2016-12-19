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

            # delete step_det
            self._model.usr_delete(p_id)

        except Exception:
            self._logger.error("Delete step error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True
