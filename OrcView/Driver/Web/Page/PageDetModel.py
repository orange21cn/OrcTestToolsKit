# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibControl import ControlBase


class PageDetControl(ControlBase):

    def __init__(self, p_def='PageDet'):

        ControlBase.__init__(self, p_def)


class PageDetModel(ModelTable):

    def __init__(self, p_def='PageDet'):

        ModelTable.__init__(self, p_def)

        self.__logger = LogClient()
        self.__resource_page_det = OrcResource("PageDet")

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_page_det.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增页面信息", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"新增页面信息", self.__logger)

        return dict(page_id=result.data["page_id"])

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_page_det.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除页面信息", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除页面信息", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        result = self.__resource_page_det.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新页面信息", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新页面信息", self.__logger)

        return result.status

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource_page_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询页面信息", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询页面信息", self.__logger)

        return result.data
