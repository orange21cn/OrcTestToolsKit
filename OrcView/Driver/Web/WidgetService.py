# coding=utf-8
from OrcLib.LibNet import OrcHttpNewResource
from OrcLib.LibLog import OrcLog


class WidgetDefService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.widget_def")
        self.__resource_page_def = OrcHttpNewResource("WidgetDef")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        return self.__resource_page_def.post(p_data)

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
        return self.__resource_page_def.put(p_data)

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return self.__resource_page_def.get(p_cond)


class WidgetDetService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.widget_det")
        self.__resource_page_det = OrcHttpNewResource("WidgetDet")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        return self.__resource_page_det.post(p_data)

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
        return self.__resource_page_det.put(p_data)

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return self.__resource_page_det.get(p_cond)
