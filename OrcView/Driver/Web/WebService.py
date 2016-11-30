# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcHttpNewResource


class WebMainService:
    """

    """
    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.web_main")

        self.__resource_page_def = OrcHttpNewResource("PageDef")
        self.__resource_page_det = OrcHttpNewResource("PageDet")
        self.__resource_widget_def = OrcHttpNewResource("WidgetDef")
        self.__resource_widget_det = OrcHttpNewResource("WidgetDet")

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
        """
        获取控件类型
        :param p_id:
        :return:
        """
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

        self.__resource_page_def.set_path(p_id)
        page_def_data = self.__resource_page_def.get()

        if page_def_data:
            return WebPageDef(page_def_data)
        else:
            return None

    def get_page_det(self, p_id):
        """
        获取页面定义
        :param p_id:
        :return:
        :rtype: WebPageDet
        """
        from OrcLib.LibDatabase import WebPageDet

        self.__resource_page_det.set_path(p_id)
        page_det_data = self.__resource_page_det.get()

        if page_det_data:
            return WebPageDet(page_det_data)
        else:
            return None

    def get_widget_def(self, p_id):
        """
        获取控件定义
        :param p_id:
        :return:
        :rtype: WebWidgetDef
        """
        from OrcLib.LibDatabase import WebWidgetDef

        self.__resource_widget_def.set_path(p_id)
        widget_def_data = self.__resource_widget_def.get()

        if widget_def_data:
            return WebWidgetDef(widget_def_data)
        else:
            return None

    def get_widget_det(self, p_id):
        """
        获取控件细节
        :param p_id:
        :return: WebWidgetDet
        """
        from OrcLib.LibDatabase import WebWidgetDet

        self.__resource_widget_det.set_path(p_id)
        widget_det_data = self.__resource_widget_det.get()

        if widget_det_data:
            return WebWidgetDet(widget_det_data)
        else:
            return None
