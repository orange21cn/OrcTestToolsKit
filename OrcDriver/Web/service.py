# coding=utf-8
from OrcLib import get_config
from OrcLib.LibNet import orc_invoke
from OrcLib.LibLog import OrcLog

_logger = OrcLog("api.driver.service")


class DriverService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("api.driver.service")

        # Get url from configuration
        _url = get_config("interface").get_option("DRIVER", "url")

        self.__url_page = '%s/Page' % _url
        self.__url_widget = '%s/Widget' % _url

    def page_get_url(self, p_id):
        """
        获取页面 url
        :param p_id: page detail id
        :return: url/None
        """
        _para = dict(id=p_id)
        return orc_invoke('%s/usr_get_url' % self.__url_page, _para)

    def widget_get_definition(self, p_id):
        """
        获取控件定义
        :param p_id:
        :return: definition list or None
        """
        _para = dict(id=p_id)
        return orc_invoke('%s/usr_get_def' % self.__url_widget, _para)

    def widget_get_detail(self, p_id):
        """
        获取定义细节
        :param p_id: widget definition id (not detail id)
        :return:
        """
        _para = dict(widget_id=p_id)
        return orc_invoke('%s/usr_get_det' % self.__url_widget, _para)
