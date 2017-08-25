# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibLog import OrcLog
from OrcLib.LibDatabase import WebWidgetDef
from OrcLib.LibDatabase import WebWidgetDet


class WebDriverService(object):

    def __init__(self):

        object.__init__(self)

        # Log
        self.__logger = OrcLog("resource.driver.service")

        self.__resource_page_def = OrcResource("PageDef")
        self.__resource_page_det = OrcResource("PageDet")
        self.__resource_widget_def = OrcResource("WidgetDef")
        self.__resource_widget_det = OrcResource("WidgetDet")

    def page_get_url(self, p_env, p_id):
        """
        获取页面 url
        :param p_env:
        :param p_id: page id
        :return: url/None
        """
        result = self.__resource_page_det.get(parameter=dict(page_id=p_id, page_env=p_env))

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取页面信息", self.__logger):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u"获取页面信息", self.__logger)

        return result.data[0]["page_url"]

    def widget_get_definition(self, p_id):
        """
        获取单个控件定义
        :param p_id:
        :return: definition list or None
        """
        result = self.__resource_widget_def.get(path=p_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取控件定义", self.__logger):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u"获取控件定义", self.__logger)

        return WebWidgetDef(result.data)

    def widget_get_definition_path(self, p_id):
        """
        获取控件定义树
        :param p_id:
        :return: definition list or None
        """
        result = self.__resource_widget_def.get(parameter=dict(type="path", id=p_id))

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取控件定义树", self.__logger):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u"获取控件定义树", self.__logger)

        return [WebWidgetDef(item) for item in result.data]

    def widget_get_detail(self, p_id):
        """
        获取定义细节
        :param p_id: widget definition id (not detail id)
        :return:
        """
        result = self.__resource_widget_det.get(parameter=dict(widget_id=p_id))

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取控件信息", self.__logger):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u"获取控件信息", self.__logger)

        return [WebWidgetDet(_item) for _item in result.data]
