# coding=utf-8
from OrcLib import get_config
from OrcLib.LibNet import orc_invoke
from OrcLib.LibNet import OrcInvoke
from OrcLib.LibLog import OrcLog


class PageService:

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


class WindowService:
    """
    Window service
    """
    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.service.window")

        # Get url from configuration
        self.__url = get_config("interface").get_option("DRIVER", "url")

        self.__invoker = OrcInvoke()

    def usr_add(self, p_data):
        """
        把存在于 widget 表但在 window 表中不存在的 window 增加到 window 表
        :param p_data:
        :return:
        """
        from OrcLib.LibNet import orc_invoke

        _url_window = '%s/api/1.0/Window' % self.__url
        _url_widget = '%s/WidgetDef/usr_search' % self.__url

        _windows_all = [item["id"] for item in orc_invoke(_url_widget, dict(widget_type="WINDOW"))]
        _windows_exist = [item["id"] for item in self.__invoker.get(_url_window)]

        for _id in _windows_all:
            if _id not in _windows_exist:
                self.__invoker.post("%s/%s" % (_url_window, _id))

    def usr_delete(self, p_list):
        """
        :param p_list:
        :return:
        """
        _url = '%s/api/1.0/Window' % self.__url
        self.__invoker.delete(_url, p_list)

    def usr_update(self, p_data):
        """
        :param p_data:
        :return:
        """
        _id = p_data["id"]
        _url = '%s/api/1.0/Window/%s' % (self.__url, _id)
        self.__invoker.put(_url, p_data)

    def usr_search(self, p_cond):
        """
        :param p_cond:
        :return:
        """
        from OrcLib.LibNet import orc_invoke

        _cond = p_cond
        _url_window = '%s/api/1.0/Window' % self.__url
        _url_widget = '%s/WidgetDef/usr_search' % self.__url

        # 有 window_flag 条件先查 widget
        if "window_flag" in _cond:
            _ids = [item["id"] for item in orc_invoke(_url_widget, dict(widget_flag=_cond["window_flag"]))]
            _cond["id"] = _ids

        # 查询
        _data = self.__invoker.get(_url_window, _cond)
        _window_list = orc_invoke(_url_widget, dict(widget_type="WINDOW"))

        def _get_widget(p_id):
            for _item in _window_list:
                if _item["id"] == p_id:
                    return _item
            return None

        if _data is None:
            return []
        else:
            for _window in _data:

                _widget = _get_widget(_window["id"])

                if _widget is not None:

                    _window["window_flag"] = _widget["widget_flag"]

            return _data


class WebMainService:
    """

    """
    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.web_main")

        # Get url from configuration
        self.__url = get_config("interface").get_option("DRIVER", "url")

        self.__invoker = OrcInvoke()

    def get_page_key(self, p_id):
        """
        获取界面显示页面标识
        :param p_id:
        :type p_id: str
        :return:
        :rtype: str
        """
        _page_det = self.get_page_det(p_id)
        _page_def = self.get_page_def(_page_det.page_id)

        return _page_def.id, _page_def.page_flag, _page_det.page_env

    def get_widget_key(self, p_id):
        """
        获取界面显示控件标识
        :param p_id:
        :type p_id: str
        :return:
        :rtype: str
        """
        _widget_def = self.get_widget_def(p_id)

        return _widget_def.widget_path

    def get_widget_type(self, p_id):

        _type_value = self.get_widget_def(p_id).widget_type

        return _type_value

    def get_page_def(self, p_id):
        """
        获取页面定义
        :param p_id:
        :return:
        :rtype: WebPageDef
        """
        from OrcLib.LibDatabase import WebPageDef

        _url_page_def = "%s/PageDef/usr_search" % self.__url
        _data = orc_invoke(_url_page_def, dict(id=p_id))

        if 0 == len(_data):
            return None

        return WebPageDef(_data[0])

    def get_page_det(self, p_id):
        """
        获取页面定义
        :param p_id:
        :return:
        :rtype: WebPageDet
        """
        from OrcLib.LibDatabase import WebPageDet

        _url_page_det = "%s/PageDet/usr_search" % self.__url
        _data = orc_invoke(_url_page_det, dict(id=p_id))

        if 0 == len(_data):
            return None

        return WebPageDet(_data[0])

    def get_widget_def(self, p_id):
        """
        获取控件定义
        :param p_id:
        :return:
        :rtype: WebWidgetDef
        """
        from OrcLib.LibDatabase import WebWidgetDef

        _url_widget_def = "%s/WidgetDef/usr_search" % self.__url
        _data = orc_invoke(_url_widget_def, dict(id=p_id))

        if 0 == len(_data):
            return None

        return WebWidgetDef(_data[0])

    def get_widget_det(self, p_id):
        """
        获取控件细节
        :param p_id:
        :return: WebWidgetDet
        """
        from OrcLib.LibDatabase import WebWidgetDet

        _url_widget_det = "%s/WidgetDet/usr_search" % self.__url
        _data = orc_invoke(_url_widget_det, dict(id=p_id))

        if 0 == len(_data):
            return None

        return WebWidgetDet(_data[0])