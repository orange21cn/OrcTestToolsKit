from OrcLib import get_config
from OrcLib.LibNet import orc_invoke


class DriverService:

    def __init__(self):

        _url = get_config("interface").get_option("DRIVER", "url")

        self.__url_page = '%s/Page' % _url
        self.__url_widget = '%s/Widget' % _url

    def page_get_url(self, p_para):
        return orc_invoke('%s/usr_get_url' % self.__url_page, p_para)

    def page_search(self, p_para):
        return orc_invoke('%s/usr_search' % self.__url_page, p_para)

    def widget_get_definition(self, p_para):
        return orc_invoke('%s/usr_get_def' % self.__url_page, p_para)

    def widget_get_detail(self, p_para):
        return orc_invoke('%s/usr_get_det' % self.__url_page, p_para)
