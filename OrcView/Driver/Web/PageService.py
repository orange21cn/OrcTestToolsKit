# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibLog import OrcLog
from OrcView.Lib.LibView import ResourceCheck


class PageDefService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.page_def")
        self.__resource_page_def = OrcResource("PageDef")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_page_def.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"增加页面"):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u" 增加页面")

        return dict(id=result.data["id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_page_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除页面"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除页面")

        return result.status

    def usr_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        result = self.__resource_page_def.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新页面"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新页面")

        return result.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource_page_def.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询页面"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询页面")

        return result.data


class PageDetService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.page_det")
        self.__resource_page_det = OrcResource("PageDet")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_page_det.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增页面信息"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"新增页面信息")

        return dict(page_id=result.data["page_id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_page_det.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除页面信息"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除页面信息")

        return result.status

    def usr_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        result = self.__resource_page_det.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新页面信息"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新页面信息")

        return result.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource_page_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询页面信息"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询页面信息")

        return result.data
