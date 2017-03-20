# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTable import StaticModelTable


class PageDefModel(StaticModelTable):

    def __init__(self):

        StaticModelTable.__init__(self, 'PageDef')

        self.__logger = LogClient()
        self.__resource_page_def = OrcResource("PageDef")

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_page_def.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"增加页面", self.__logger):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u" 增加页面", self.__logger)

        return dict(id=result.data["id"])

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_page_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除页面", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除页面", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        result = self.__resource_page_def.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新页面", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新页面", self.__logger)

        return result.status

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource_page_def.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询页面", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询页面", self.__logger)

        return result.data