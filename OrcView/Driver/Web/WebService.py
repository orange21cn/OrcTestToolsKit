# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcView.Lib.LibView import ResourceCheck


class WebMainService:
    """

    """
    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.web_main")

        self.__resource_page_def = OrcResource("PageDef")
        self.__resource_page_det = OrcResource("PageDet")
        self.__resource_widget_def = OrcResource("WidgetDef")
        self.__resource_widget_det = OrcResource("WidgetDet")

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

        result = self.__resource_page_def.get(path=p_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取页面定义"):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u" 获取页面定义")

        return WebPageDef(result.data)

    def get_page_det(self, p_id):
        """
        获取页面信息
        :param p_id:
        :return:
        :rtype: WebPageDet
        """
        from OrcLib.LibDatabase import WebPageDet

        result = self.__resource_page_det.get(path=p_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取页面信息"):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u" 获取页面信息")

        return WebPageDet(result.data)

    def get_widget_def(self, p_id):
        """
        获取控件定义
        :param p_id:
        :return:
        :rtype: WebWidgetDef
        """
        from OrcLib.LibDatabase import WebWidgetDef

        result = self.__resource_widget_def.get(path=p_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取控件定义"):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u" 获取控件定义")

        return WebWidgetDef(result.data)

    def get_widget_det(self, p_id):
        """
        获取控件细节
        :param p_id:
        :return: WebWidgetDet
        """
        from OrcLib.LibDatabase import WebWidgetDet

        result = self.__resource_widget_det.get(path=p_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取控件细节"):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u" 获取控件细节")

        return WebWidgetDet(result.data)
