# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTable import StaticModelTable


class WidgetDetModel(StaticModelTable):

    def __init__(self):

        StaticModelTable.__init__(self, 'WidgetDet')

        self.__logger = LogClient()
        self.__resource_widget_det = OrcResource("WidgetDet")

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_widget_det.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增控件属性", self.__logger):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增控件属性", self.__logger)

        return dict(widget_id=result.data["widget_id"])

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_widget_det.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除控件属性", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除控件属性", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        result = self.__resource_widget_det.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新控件属性", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新控件属性", self.__logger)

        return result.status

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource_widget_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询控件属性", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询控件属性", self.__logger)

        return result.data

    def service_up(self, p_id):
        """
        上移
        :param p_id:
        :return:
        """
        result = self.__resource_widget_det.post(path=p_id, parameter=dict(cmd="up"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"上移步骤", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"上移步骤", self.__logger)

        return result.status

    def service_down(self, p_id):
        """
        下移
        :param p_id:
        :return:
        """
        result = self.__resource_widget_det.post(path=p_id, parameter=dict(cmd="down"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"下移步骤", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"下移步骤", self.__logger)

        return result.status