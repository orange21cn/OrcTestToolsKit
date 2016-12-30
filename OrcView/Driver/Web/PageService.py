# coding=utf-8
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibLog import OrcLog


class PageDefService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.page_def")
        self.__resource_page_def = OrcHttpResource("PageDef")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        page_data = self.__resource_page_def.post(p_data)
        return dict(id=page_data["id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        return self.__resource_page_def.delete(p_list)

    def usr_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        self.__resource_page_def.set_path(p_data["id"])
        return self.__resource_page_def.put(p_data)

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return self.__resource_page_def.get(p_cond)


class PageDetService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.page_det")
        self.__resource_page_det = OrcHttpResource("PageDet")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        page_det_data = self.__resource_page_det.post(p_data)
        return dict(page_id=page_det_data["page_id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        return self.__resource_page_det.delete(p_list)

    def usr_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        self.__resource_page_det.set_path(p_data["id"])
        return self.__resource_page_det.put(p_data)

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return self.__resource_page_det.get(p_cond)

    # def page_get_url(self, p_id):
    #     """
    #     获取页面 url
    #     :param p_id: page detail id
    #     :return: url/None
    #     """
    #     self.__resource_page_det.set_path(p_id)
    #     page_det_data = self.__resource_page_det.get()
    #
    #     return None if not page_det_data else page_det_data["page_url"]
