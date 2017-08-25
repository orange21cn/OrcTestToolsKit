# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibControl import ControlBase


class BatchDefControl(ControlBase):

    def __init__(self, p_def):

        ControlBase.__init__(self, p_def)


class BatchDefModel(ModelTree):

    def __init__(self, p_def='BatchDef'):

        ModelTree.__init__(self, p_def)

        self.__logger = LogClient()

        self.__resource_batch_def = OrcResource("BatchDef")
        self.__resource_run_def = OrcResource("RunDef")

    def service_add(self, p_data):
        """
        增加
        :param p_data:
        :return:
        """
        result = self.__resource_batch_def.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增计划", self.__logger):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增计划", self.__logger)

        return dict(id=result.data["id"])

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_batch_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除计划", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"新增计划", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        result = self.__resource_batch_def.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新计划", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新计划", self.__logger)

        return result.status

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        cond = dict(type="all")
        cond.update(p_cond)

        result = self.__resource_batch_def.get(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询计划", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询计划", self.__logger)

        return result.data

    def service_run(self, p_id):
        """
        加入运行列表
        :param p_id:
        :return:
        """
        cond = dict(id=p_id, run_def_type="BATCH")
        result = self.__resource_run_def.post(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"添加至运行", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"添加至运行", self.__logger)

        return True
