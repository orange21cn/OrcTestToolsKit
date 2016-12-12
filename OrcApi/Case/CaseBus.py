# coding=utf-8
from OrcLib import init_log
from OrcLib.LibNet import OrcLog
from OrcLib.LibException import OrcApiModelFailException
from CaseDefMod import CaseDefMod
from CaseDetMod import CaseDetMod
from StepBus import StepDefBus


class CaseDefBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.case.bus.case_def")
        self.__model_case_def = CaseDefMod()
        self.__bus_case_det = CaseDetBus()

    def bus_list_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        try:
            result = self.__model_case_def.usr_add(p_data)
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
            self.__logger.error("Delete case error, input: %s" % p_list)
            raise OrcApiModelFailException

        return True

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
                result = self.__model_case_def.usr_search_all(p_cond)

            # 查询用例及子节点
            elif "tree" == mode:
                if case_id is not None:
                    result = self.__model_case_def.usr_search_tree(case_id)

            # 查询用例路径
            elif "path" == mode and case_id:
                if case_id is not None:
                    result = self.__model_case_def.usr_search_path(case_id)

            # 其他情况只查询符合条件的数据
            else:
                result = self.__model_case_def.usr_search(p_cond)

        except OrcApiModelFailException:
            self.__logger.error("Search case error, input: %s" % p_cond)
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
            case_det_list.extend(self.__bus_case_det.bus_list_search(dict(case_id=_case_id)))
        case_det_id_list = [item.id for item in case_det_list]

        try:
            # 删除 case_det
            self.__bus_case_det.bus_list_delete(case_det_id_list)

            # 删除 case
            for _id in case_id_list:
                self.__model_case_def.usr_delete(_id)

        except Exception:
            self.__logger.error("Delete batch error, input: %s" % p_id)
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
            self.__model_case_def.usr_update(cond)
        except Exception:
            self.__logger.error("Update batch error, input: %s" % cond)
            raise OrcApiModelFailException

    def bus_search(self, p_id):
        """
        查询单个用例
        :param p_id:
        :return:
        """
        try:
            result = self.__model_case_def.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Search batch error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result


class CaseDetBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.case.bus.case_det")
        self.__model_case_det = CaseDetMod()
        self.__bus_step_def = StepDefBus()

    def bus_list_add(self, p_data):
        """
        查询
        :param p_data:
        :return:
        """
        try:
            result = self.__model_case_det.usr_add(p_data)
        except Exception:
            self.__logger.error("Add batch error, input: %s" % p_data)
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
            self.__logger.error("Delete batch error, input: %s" % p_list)
            raise OrcApiModelFailException

        return True

    def bus_list_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_case_det.usr_search(p_cond)
        except Exception:
            self.__logger.error("Search batch error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        try:
            # case det
            case_det = self.__model_case_det.usr_search(dict(id=p_id))

            # step ids
            step_ids = [step.step_id for step in case_det]

            # delete steps
            self.__bus_step_def.bus_list_delete(step_ids)

            # delete case det
            self.__model_case_det.usr_delete(p_id)

        except Exception:
            self.__logger.error("Del case from batch error, input: %s" % p_id)
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
            self.__model_case_det.usr_update(cond)
        except Exception:
            self.__logger.error("Update case error, input: %s" % cond)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询
        :param p_id:
        :return:
        """
        try:
            result = self.__model_case_det.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Search case from batch error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result
