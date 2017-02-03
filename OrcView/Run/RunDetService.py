# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcView.Lib.LibView import ResourceCheck


class RunDetService():

    def __init__(self):

        self.__resource_run_det = OrcResource("RunDet")
        self.__resource_run = OrcResource("Run")

    def usr_search(self, p_path):
        """
        查询
        :param p_path:
        :return:
        """
        result = self.__resource_run_det.get(parameter=p_path)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询测试清单"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询测试清单")

        return result.data

    def usr_run(self, p_path):

        result = self.__resource_run.put(p_path)

        # 检查结果
        if not ResourceCheck.result_status(result, u"执行测试"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"执行测试")

        return result.status
