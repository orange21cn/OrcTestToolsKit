# coding=utf-8
from OrcLib.LibApi import OrcBus
from OrcLib.LibException import OrcApiModelFailException

from BatchDefMod import BatchDefMod
from BatchDetMod import BatchDetMod
from OrcApi.Case.CaseBus import CaseDefBus


class BatchDefBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "batch_def", BatchDefMod)

        self._bus_batch_det = BatchDetBus()
        self._bus_case_def = CaseDefBus()

    def bus_list_search(self, p_cond):
        """
        查询 list
        :param p_cond:
        :return:
        """
        result = []

        mode = p_cond["type"] if "type" in p_cond else None
        batch_id = p_cond["id"] if "id" in p_cond else None

        try:
            # 查询符合条件的整用例树,至根节点
            if "all" == mode:
                result = self._model.usr_search_all(p_cond)

            # 查询节点及子节点
            elif "tree" == mode:
                if batch_id is not None:
                    result = self._model.usr_search_tree(batch_id)

            # 查询节点路径
            elif "path" == mode:
                if batch_id is not None:
                    result = self._model.usr_search_path(batch_id)

            # 其他情况只查询符合条件的数据
            else:
                result = self._model.usr_search(p_cond)

        except Exception:
            self._logger.error("Search batch error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_delete(self, p_id):
        """
        删除一条
        :param p_id:
        :return:
        """
        # 查询 batch 列表, 包含子节点
        batch_list = self.bus_list_search(dict(type="tree", id=p_id))
        batch_id_list = [item.id for item in batch_list]

        # 查询 batch_det 列表
        batch_det_list = []
        for _batch_id in batch_id_list:
            batch_det_list.extend(self._bus_batch_det.bus_list_search(dict(batch_id=_batch_id)))
        batch_det_id_list = [item.id for item in batch_det_list]

        try:
            # 删除 batch_det
            self._bus_batch_det.bus_list_delete(batch_det_id_list)

            # 删除 batch
            for _id in batch_id_list:
                self._model.usr_delete(_id)

        except Exception:
            self._logger.error("Delete batch error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True


class BatchDetBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "batch_det", BatchDetMod)
