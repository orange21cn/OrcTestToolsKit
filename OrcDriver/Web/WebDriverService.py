# coding=utf-8
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibLog import OrcLog
from OrcLib.LibDatabase import WebWidgetDef
from OrcLib.LibDatabase import WebWidgetDet


class WebDriverService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("api.driver.service")

        self.__resource_page_def = OrcHttpResource("PageDef")
        self.__resource_page_det = OrcHttpResource("PageDet")
        self.__resource_widget_def = OrcHttpResource("WidgetDef")
        self.__resource_widget_det = OrcHttpResource("WidgetDet")

    def page_get_url(self, p_env, p_id):
        """
        获取页面 url
        :param p_env:
        :param p_id: page id
        :return: url/None
        """
        page_det_datas = self.__resource_page_det.get(dict(page_id=p_id, page_env=p_env))
        return None if not page_det_datas else page_det_datas[0]["page_url"]

    def widget_get_definition(self, p_id):
        """
        获取单个控件定义
        :param p_id:
        :return: definition list or None
        """
        self.__resource_widget_def.set_path(p_id)
        widget_def_data = self.__resource_widget_def.get()
        return None if not widget_def_data else WebWidgetDef(widget_def_data)

    def widget_get_definition_path(self, p_id):
        """
        获取控件定义树
        :param p_id:
        :return: definition list or None
        """
        widget_def_datas = self.__resource_widget_def.get(dict(type="path", id=p_id))
        return None if not widget_def_datas else [WebWidgetDef(item) for item in widget_def_datas]

    def widget_get_detail(self, p_id):
        """
        获取定义细节
        :param p_id: widget definition id (not detail id)
        :return:
        """
        widget_det_data = self.__resource_widget_det.get(dict(widget_id=p_id))
        return None if not widget_det_data else [WebWidgetDet(_item) for _item in widget_det_data]
