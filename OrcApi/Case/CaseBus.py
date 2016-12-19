# coding=utf-8
from OrcLib.LibApi import OrcBus
from OrcLib.LibException import OrcApiModelFailException

from CaseDefMod import CaseDefMod
from CaseDetMod import CaseDetMod
from StepBus import StepDefBus


class CaseDefBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "case_def", CaseDefMod)

        self._bus_case_det = CaseDetBus()

    def bus_list_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = []

        mode = p_cond["type"] if "type" in p_cond else None
        case_id = p_cond["id"] if "id" in p_cond else None

        try:
            # 查询符合条件的整用例树,至根节点
            if "all" == mode:
                result = self._model.usr_search_all(p_cond)

            # 查询用例及子节点
            elif "tree" == mode:
                if case_id is not None:
                    result = self._model.usr_search_tree(case_id)

            # 查询用例路径
            elif "path" == mode and case_id:
                if case_id is not None:
                    result = self._model.usr_search_path(case_id)

            # 其他情况只查询符合条件的数据
            else:
                result = self._model.usr_search(p_cond)

        except OrcApiModelFailException:
            self._logger.error("Search case_def error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_delete(self, p_id):
        """
        删除单个用例
        :param p_id:
        :return:
        """
        # 查询 case 列表, 包含子节点
        case_list = self.bus_list_search(dict(type="tree", id=p_id))
        case_id_list = [item.id for item in case_list]

        # 查询 step 列表
        case_det_list = []
        for _case_id in case_id_list:
            case_det_list.extend(self._bus_case_det.bus_list_search(dict(case_id=_case_id)))
        case_det_id_list = [item.id for item in case_det_list]

        try:
            # 删除 case_det
            self._bus_case_det.bus_list_delete(case_det_id_list)

            # 删除 case
            for _id in case_id_list:
                self._model.usr_delete(_id)

        except Exception:
            self._logger.error("Delete case_def error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True


class CaseDetBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "case_det", CaseDetMod)

        self._bus_step_def = StepDefBus()

    def bus_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        try:
            # case det
            case_det = self._model.usr_search(dict(id=p_id))

            # step ids
            step_ids = [step.step_id for step in case_det]

            # delete steps
            self._bus_step_def.bus_list_delete(step_ids)

            # delete case det
            self._model.usr_delete(p_id)

        except Exception:
            self._logger.error("Del case_det error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True
