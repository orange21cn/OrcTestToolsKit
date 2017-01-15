# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibLog import OrcLog
from OrcView.Lib.LibView import ResourceCheck


class WidgetDefService:

    def __init__(self):

        self.__logger = OrcLog("view.driver.web.service.widget_def")
        self.__resource_widget_def = OrcResource("WidgetDef")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_widget_def.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"增加控件"):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"增加控件")

        return dict(id=result.data["id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_widget_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除控件"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除控件")

        return result.status

    def usr_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        result = self.__resource_widget_def.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新控件"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新控件")

        return result.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        cond = dict(type="all")
        cond.update(p_cond)
        result = self.__resource_widget_def.get(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询控件"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询控件")

        return result.data


class WidgetDetService:

    def __init__(self):

        self.__logger = OrcLog("view.driver.web.service.widget_det")
        self.__resource_widget_det = OrcResource("WidgetDet")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_widget_det.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增控件属性"):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增控件属性")

        return dict(widget_id=result.data["widget_id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_widget_det.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除控件属性"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除控件属性")

        return result.status

    def usr_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        result = self.__resource_widget_det.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新控件属性"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新控件属性")

        return result.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource_widget_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询控件属性"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询控件属性")

        return result.data

    def usr_up(self, p_id):
        """
        上移
        :param p_id:
        :return:
        """
        result = self.__resource_widget_det.post(path=p_id, parameter=dict(cmd="up"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"上移步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"上移步骤")

        return result.status

    def usr_down(self, p_id):
        """
        下移
        :param p_id:
        :return:
        """
        result = self.__resource_widget_det.post(path=p_id, parameter=dict(cmd="down"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"下移步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"下移步骤")

        return result.status
