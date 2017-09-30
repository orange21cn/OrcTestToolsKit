# coding=utf-8
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from OrcApi.OrcDriver.Web.WebDriverService import WebDriverService
from OrcLib.LibLog import OrcLog
from OrcLib.LibCmd import WebCmd
from OrcLibFrame.LibRunTime import OrcRunTime


class OrcWidget(object):
    """
    控件基类
    """
    def __init__(self, p_root, p_id):

        object.__init__(self)

        self._logger = OrcLog('driver.web')

        # 根,驱动本身
        self._root = p_root

        # 控件
        self._widget = p_root


class WidgetBlock(object):
    """
    控件基类
    """
    def __init__(self, p_root, p_id):
        """
        :param p_root:
        :param p_id:
        :return:
        """
        object.__init__(self)

        self._logger = OrcLog('driver.web')

        # 根,驱动本身
        self._root = p_root

        # 控件
        self._widget = p_root

        # 是否遇到 frame,下一步将执行 switch_to
        self.__meet_frame = False

        # 服务用于调用其他模块
        self.__service = WebDriverService()

        # 实时数据
        self.__runtime = OrcRunTime('RUN')

        # id 数组/兼容多控件操作
        self._ids = str(p_id).split('|')

        # 控件定义
        self._def = self.__get_def_info(self._ids[0])

        # 获取控件
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

        for i in range(10):

            try:
                self._get_widget()
                self._widget.is_displayed()
                break
            except (NoSuchElementException, AttributeError):
                pass
        else:
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
                self.set_frame(self.__meet_frame)

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
            elif 'LAST_CHILD' == _type:
                self._widget = self.__get_child(_attr)
            else:
                pass

    def __get_child(self, p_tag):
        """
        获取子节点
        :return:
        """
        result = self._root.find_elements_by_tag_name(p_tag)
        return result[len(result) - 1]

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

    def basic_execute(self, p_para):
        """
        基本控件操作
        :param p_para:
        :type p_para: WebCmd
        :return:
        """
        # 判断存在
        if 'EXISTS' == p_para.cmd_operation:
            return self.exists()

        # 点击
        elif 'CLICK' == p_para.cmd_operation:

            try:
                self._widget.click()
            except TimeoutException:
                self._root.execute_script('window.stop()')
            except ElementNotInteractableException:
                return False

            return True

        # 获取属性
        elif 'GET_ATTR' == p_para.cmd_operation:
            return self._widget.get_attribute(p_para.data_inp[0])

        # 获取内容
        elif 'GET_TEXT' == p_para.cmd_operation:
            return self._widget.text

        # 获取HTML
        elif 'GET_HTML' == p_para.cmd_operation:
            return self._widget.get_attribute("outerHTML")

        # 滚动至显示区
        elif 'SCROLL' == p_para.cmd_operation:
            self._root.execute_script("arguments[0].scrollIntoView();", self._widget)

        # Focus
        elif 'FOCUS' == p_para.cmd_operation:
            self._root.execute_script("arguments[0].focus();", self._widget)

        elif 'SET_ATTR' == p_para.cmd_operation:
            js_cmd = "setAttribute('%s', '%s')" % (p_para.data_inp[0], p_para.data_inp[1])
            self._root.execute_script("arguments[0].%s;" % js_cmd, self._widget)

        elif 'DEL_ATTR' == p_para.cmd_operation:
            js_cmd = "removeAttribute('%s')" % p_para.data_inp[0]
            self._root.execute_script("arguments[0].%s;" % js_cmd, self._widget)

        # 双击
        elif 'DOUBLE_CLICK' == p_para.cmd_operation:
            ActionChains(self._root).double_click(self._widget).perform()

        # 右键
        elif 'CONTEXT' == p_para.cmd_operation:
            ActionChains(self._root).context_click(self._widget).perform()

        elif 'MOVE' == p_para.cmd_operation:
            ActionChains(self._root).drag_and_drop_by_offset(self._widget, p_para.data_inp[0], p_para.data_inp[1])

        # ----
        elif 'DEL_ATTR' == p_para.cmd_operation:
            js_cmd = "removeAttribute('%s')" % p_para.data_inp[0]
            self._root.execute_script("arguments[0].%s;" % js_cmd, self._widget)

        elif 'SCRIPT' == p_para.cmd_operation:
            self._root.execute_script("arguments[0].%s;" % p_para.data_inp[0], self._widget)

        else:
            return None
