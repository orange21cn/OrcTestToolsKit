# coding=utf-8
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from OrcDriver.Web.WebDriverService import WebDriverService
from OrcLib.LibLog import OrcLog
from OrcLib.LibRunTime import OrcRunTime


class OrcWidget:
    """
    控件基类
    """
    def __init__(self, p_root, p_id):

        self._logger = OrcLog('driver.web')

        self._root = p_root
        self._widget = p_root

        # 是否遇到 frame,下一步将执行 switch_to
        self.__meet_frame = False

        self.__service = WebDriverService()
        self.__runtime = OrcRunTime('RUN')

        self._def = self.__get_def_info(p_id)
        self._get_widget()

    # 标识当前的 frame id
    def get_frame(self):
        """
        设置 frame
        :return:
        """
        return bool(self.__runtime.get_value('FRAME'))

    def set_frame(self, p_value):
        """
        获取 frame
        :param p_value:
        :return:
        """
        self.__runtime.set_value('FRAME', p_value)

    # 标识当前的 window id
    def get_window(self):
        """
        设置 window
        :return:
        """
        return bool(self.__runtime.get_value('WINDOW'))

    def set_window(self, p_value):
        """
        获取 window
        :param p_value:
        :return:
        """
        self.__runtime.set_value('FRAME', p_value)

    def __get_def_info(self, p_id):
        """
        获取对象定义
        :rtype: list
        :param p_id:
        :return:
        """
        _definition = list()

        # Get definition
        _widget_def = self.__service.widget_get_definition_path(p_id)

        if _widget_def is None:
            return None

        # Get detail
        for t_def in _widget_def:
            _widget_det = self.__service.widget_get_detail(t_def.id)
            _definition.append(dict(DEF=t_def, DET=_widget_det))

        return _definition

    def exists(self):
        """
        检查控件是否显示
        :return:
        """
        if self._widget is None:
            return False

        try:
            self._widget.is_displayed()
        except NoSuchElementException:
            return False

        return True

    def _get_widget(self):
        """
        获取对象,处理 frame 和 window 跳转
        :return:
        """
        if self._root is None or self._def is None:
            return None

        if self.get_frame():
            self._root.switch_to_default_content()
            self._widget = self._root

        for t_def in self._def:

            _definition = t_def["DEF"]
            _detail = t_def["DET"]

            if _detail is None:
                continue

            # 上一级是 frame,首先进行跳转
            if self.__meet_frame:

                self._root.switch_to.frame(self._widget)
                self._widget = self._root

                self.__meet_frame = False
                self.frame = self.__meet_frame

            if "FRAME" == _definition.widget_type:
                self._get_object(_detail)
                self.__meet_frame = _definition.id

            elif "WINDOW" == _definition.widget_type:

                _window_id = _definition.id

                # 还没有当前 window
                if not self.window:
                    self.window = _window_id
                    continue

                # 检查是否当前 window
                if self.window == _window_id:
                    continue

                # 如果不是,切换 window
                self.__switch_window(_definition)

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
            elif "LINK_TEXT" == _type:
                self._widget = self._widget.find_element_by_link_text(_attr)
            elif "CSS" == _type:
                self._widget = self._widget.find_element_by_css_selector(_attr)
            else:
                pass

    def __switch_window(self, p_def):
        """
        切换窗口
        :param p_def:
        :return:
        """
        founded = False

        # 保存当前数据,未找到时恢复
        current_id = self.window
        current_handle = self._widget.current_window_handle

        # 当前 window 置为目标 id
        self.window = p_def["id"]

        # 切换
        for _handle in self.window.window_handles:

            if _handle == current_handle:
                continue

            self._widget.switch_to.window(_handle)
            founded = self.__check_window_handle(p_def["window_flag"])

            if founded:
                self._root.switch_to_window(_handle)
                break

        if not founded:
            self._widget = None
            self.window = current_id

        return founded

    def __check_window_handle(self, p_flags):
        """
        检查当前window是否所需window
        :param p_flags:[{TYPE, DATA}, ...]
        :return:
        """
        status = True

        for _flg in p_flags:

            if "TITLE" == _flg["TYPE"]:
                status = _flg["DATA"] != self._widget.title

            elif "WIDGET" == _flg["TYPE"]:
                status = OrcWidget(self._widget, _flg["DATA"]).exists()
            else:
                status = False

        return status

    def __check_object(self, p_time=20):
        """
        加载判断函数，加载页面直至 p_item_id 控件出现
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

    def basic_execute(self, p_para):
        """
        基本控件操作
        :param p_para:
        :return:
        """
        _flag = p_para["OPERATION"]

        # 判断存在
        if "EXISTS" == _flag:
            return self.exists()

        # 点击
        elif "CLICK" == _flag:
            try:
                self._widget.click()
            except TimeoutException:
                self._root.execute_script('window.stop()')
            return True

        # 获取属性
        elif "GET_ATTR" == _flag:

            if "DATA" not in p_para:
                return ""
            else:
                return self._widget.get_attribute(p_para["DATA"])

        # 获取内容
        elif "GET_TEXT" == _flag:
            return self._widget.text

        # 获取HTML
        elif "GET_HTML" == _flag:
            return self._widget.get_attribute("outerHTML")

        # 检查控件存在
        elif "DISPLAY" == _flag:
            return self.__check_object()

        else:
            return None
