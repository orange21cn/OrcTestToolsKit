# coding=utf-8
from OrcLib import init_log
from OrcLib.LibNet import OrcLog
from OrcLib.LibApi import connect_list
from OrcLib.LibException import OrcApiModelFailException

from BatchDefMod import BatchDefMod
from BatchDetMod import BatchDetMod
from OrcApi.Case.CaseBus import CaseDefBus


class BatchDefBus(object):

    def __init__(self):

        object.__init__(self)

        init_log()

        self.__logger = OrcLog("api.batch.bus.batch_def")
        self.__model_batch_def = BatchDefMod()
        self.__bus_batch_det = BatchDetBus()
        self.__bus_case_def = CaseDefBus

    def bus_list_add(self, p_cond):
        """
        新增
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_batch_def.usr_add(p_cond)
        except Exception:
            self.__logger.error("Add batch error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_list_delete(self, p_list):
        """
        删除 list, 调用单个删除函数
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
                result = self.__model_batch_def.usr_search_all(p_cond)

            # 查询节点及子节点
            elif "tree" == mode:
                if batch_id is not None:
                    result = self.__model_batch_def.usr_search_tree(batch_id)

            # 查询节点路径
            elif "path" == mode:
                if batch_id is not None:
                    result = self.__model_batch_def.usr_search_path(batch_id)

            # 其他情况只查询符合条件的数据
            else:
                result = self.__model_batch_def.usr_search(p_cond)
        except Exception:
            self.__logger.error("Search batch error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_update(self, p_id, p_cond):
        """
        更新一条
        :param p_id:
        :param p_cond:
        :return:
        """
        cond = dict(id=p_id).update(p_cond)

        try:
            self.__model_batch_def.usr_update(cond)
        except Exception:
            self.__logger.error("Update batch error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return True

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
            batch_det_list.extend(self.__bus_batch_det.bus_list_search(dict(batch_id=_batch_id)))
        batch_det_id_list = [item.id for item in batch_det_list]

        try:
            # 删除 batch_det
            self.__bus_batch_det.bus_list_delete(batch_det_id_list)

            # 删除 batch
            for _id in batch_id_list:
                self.__model_batch_def.usr_delete(_id)

        except Exception:
            self.__logger.error("Delete batch error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询一条
        :param p_id:
        :return:
        """
        try:
            result = self.__model_batch_def.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Search batch error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result


class BatchDetBus(object):

    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog("api.batch.bus.batch_def")
        self.__model_batch_det = BatchDetMod()
        self.__bus_case_def = CaseDefBus()

    def bus_list_add(self, p_cond):
        """
        新增
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_batch_det.usr_add(p_cond)
        except Exception:
            self.__logger.error("Add case to batch error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_list_delete(self, p_cond):
        """
        删除 list
        :param p_cond:
        :return:
        """
        try:
            for _id in p_cond:
                self.__model_batch_det.usr_delete(_id)
        except Exception:
            self.__logger.error("Del case from batch error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return True

    def bus_list_search(self, p_cond):
        """
        查询 list
        :param p_cond:
        :return:
        """
        try:
            result = self.__model_batch_det.usr_search(p_cond)
        except Exception:
            self.__logger.error("Search batch's case error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_update(self, p_id, p_cond):
        """
        更新一条
        :param p_id:
        :param p_cond:
        :return:
        """
        cond = dict(id=p_id).update(p_cond)

        try:
            self.__model_batch_det.usr_update(cond)
        except Exception:
            self.__logger.error("Update case of batch error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return True

    def bus_delete(self, p_id):
        """
        删除一条
        :param p_id:
        :return:
        """
        try:
            self.__model_batch_det.usr_delete(p_id)
        except Exception:
            self.__logger.error("Del case from batch error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询一条
        :param p_id:
        :return:
        """
        try:
            result = self.__model_batch_det.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self.__logger.error("Search batch's case error, input: %s" % p_id)
            raise OrcApiModelFailException

        return result
