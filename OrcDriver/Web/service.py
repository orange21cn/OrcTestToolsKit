# coding=utf-8
from OrcLib import get_config
from OrcLib.LibNet import orc_invoke
from OrcLib.LibLog import OrcLog
from OrcLib.LibDatabase import WebWidgetDef
from OrcLib.LibDatabase import WebWidgetDet


class DriverService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("api.driver.service")

        # Get url from configuration
        self.__url = get_config("interface").get_option("DRIVER", "url")

    def page_get_url(self, p_id):
        """
        获取页面 url
        :param p_id: page detail id
        :return: url/None
        """
        _url = '%s/PageDet/usr_search' % self.__url
        _data = orc_invoke(_url, dict(id=p_id))

        if _data is None or 0 == len(_data):
            return None
        else:
            return _data[0]["page_url"]

    def widget_get_definition(self, p_id):
        """
        获取控件定义
        :param p_id:
        :return: definition list or None
        """
        _url = '%s/WidgetDef/usr_search' % self.__url
        _data = orc_invoke(_url, dict(id=p_id))

        if _data is None or 0 == len(_data):
            return None
        else:
            return WebWidgetDef(_data[0])

    def widget_get_definition_tree(self, p_id):
        """
        获取控件定义
        :param p_id:
        :return: definition list or None
        """
        _url = '%s/WidgetDef/usr_search_tree' % self.__url
        _data = orc_invoke(_url, dict(id=p_id))

        if _data is None or 0 == len(_data):
            return None
        else:
            return [WebWidgetDef(_item) for _item in _data]

    def widget_get_detail(self, p_id):
        """
        获取定义细节
        :param p_id: widget definition id (not detail id)
        :return:
        """
        _url = '%s/WidgetDet/usr_search' % self.__url
        _data = orc_invoke(_url, dict(widget_id=p_id))

        if _data is None or 0 == len(_data):
            return None
        else:
            return [WebWidgetDet(_item) for _item in _data]
