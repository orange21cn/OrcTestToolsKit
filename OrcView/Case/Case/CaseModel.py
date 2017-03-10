# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTree import ModelTree


class CaseModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self, 'Case')

        self.__logger = LogClient()

        self.__resource_case_def = OrcResource("CaseDef")
        self.__resource_run_def = OrcResource("RunDef")

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_case_def.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增用例", self.__logger):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增用例", self.__logger)

        return dict(id=result.data["id"])

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_case_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除用例", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除用例", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        result = self.__resource_case_def.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新用例", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新用例", self.__logger)

        return result.status

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        cond = dict(type="all")
        cond.update(p_cond)
        result = self.__resource_case_def.get(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询用例", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询用例", self.__logger)

        return result.data

    def service_run(self, p_id):
        """
        加入运行
        :param p_id:
        :return:
        """
        cond = dict(id=p_id, run_def_type="CASE")
        result = self.__resource_run_def.post(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"添加至运行", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"添加至运行", self.__logger)

        return True