# coding=utf-8
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

from OrcDriver.Web import WebSocketService
from OrcLib.LibLog import OrcLog


class OrcWidget:
    """
    控件基类
    """
    def __init__(self, p_root, p_id):

        self._logger = OrcLog("driver.web")

        self._root = p_root
        self._widget = p_root
        self._window = None
        self.__service = WebSocketService()

        self._def = self.__get_def_info(p_id)
        self._get_widget()

    def __get_def_info(self, p_id):
        """
        获取对象定义
        :rtype: list
        :param p_id:
        :return:
        """
        _definition = list()

        # Get definition
        _widget_def = self.__service.widget_get_definition_tree(p_id)

        if _widget_def is None:
            return None

        # Get detail
        for t_def in _widget_def:

            _widget_det = self.__service.widget_get_detail(t_def.id)
            _definition.append(dict(DEF=t_def, DET=_widget_det))

        return _definition

    def exists(self):
        # todo None AttributeError
        return self._widget.is_displayed()

    def _get_widget(self):
        """
        获取对象,处理 frame 和 window 跳转
        :return:
        """
        if self._root is None or self._def is None:
            return None

        self._widget = self._root

        for t_def in self._def:

            _definition = t_def["DEF"]
            _detail = t_def["DET"]

            if "FRAME" == _definition.widget_type:
                self._get_object(_detail)
                self._root.switch_to_default_content()
                self._root.switch_to.frame(self._widget)
                self._widget = self._root

            elif "WINDOW" == _definition.widget_type:
                # Todo 处理当前 window 未变放到这里
                # self.__switch_window(_detail)
                pass

            else:
                self._get_object(_detail)

    def _get_object(self, p_det):
        """
        获取对象,调用 selenium 函数
        :param p_det:
        :return:
        """
        if 0 == len(p_det):
            return None

        for t_item in p_det:

            _type = t_item.widget_attr_type
            _attr = t_item.widget_attr_value

            if "ID" == _type:
                self._widget = self._widget.find_element_by_id(_attr)
            elif "NAME" == _type:
                self._widget = self._widget.find_element_by_name(_attr)
            elif "TAG_NAME" == _type:
                self._widget = self._widget.find_element_by_tag_name(_attr)
            elif "XPATH" == _type:
                self._widget = self._widget.find_element_by_xpath(_attr)
            else:
                pass

    def __switch_window(self, p_def):
        """
        :param p_def:
        :return:
        """
        _current_window = self._window

        _definition = p_def["DEF"]
        _detail = p_def["DET"]

        if _definition.id != self._window:

            self._window = _definition.id

            _founded = False
            _current_handle = self._widget.current_window_handle
            _all_handles = self._widget.window_handles

            for t_handle in _all_handles:

                if t_handle != _current_handle:

                    self._widget.switch_to_window(t_handle)
                    self._root.switch_to_window(t_handle)

                    _founded = self.__check_object(_detail)
                    if _founded:
                        break

            if not _founded:
                self.__window = _current_window

    def __check_object(self, p_def, p_time=20):
        """
        加载判断函数，加载页面直至 p_item_id 控件出现
        :param p_def:
        :param p_time:
        :return:
        """
        _displayed = True

        def get_object(_driver, _item):
            return OrcWidget(_driver, _item)

        try:
            WebDriverWait(self._root, p_time).until(lambda _sup, _def: get_object(_sup, _def).exists())
        except WebDriverException:
            _displayed = False

        return _displayed
