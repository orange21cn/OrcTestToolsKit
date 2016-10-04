# coding=utf-8
from OrcLib import get_config
from OrcLib.LibNet import orc_invoke
from OrcLib.LibLog import OrcLog


class DriverService:

    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.service")

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