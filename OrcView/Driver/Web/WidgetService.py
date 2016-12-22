# coding=utf-8
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibLog import OrcLog


class WidgetDefService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.widget_def")
        self.__resource_widget_def = OrcHttpResource("WidgetDef")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        widget_data = self.__resource_widget_def.post(p_data)
        return dict(id=widget_data["id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        return self.__resource_widget_def.delete(p_list)

    def usr_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        self.__resource_widget_def.set_path(p_data["id"])
        return self.__resource_widget_def.put(p_data)

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        cond = dict(type="all")
        cond.update(p_cond)

        return self.__resource_widget_def.get(cond)


class WidgetDetService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.widget_det")
        self.__resource_page_det = OrcHttpResource("WidgetDet")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        widget_det_data = self.__resource_page_det.post(p_data)
        return dict(widget_id=widget_det_data["widget_id"])

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
