# coding=utf-8
import time
import time
import multiprocessing
from multiprocessing import queues
from time import sleep

from OrcApi.OrcDriver.Web.Widget.OrcWidget import WidgetBlock
from OrcApi.OrcDriver.Web.Widget.WidgetA import WidgetA
from OrcApi.OrcDriver.Web.Widget.WidgetAlert import WidgetAlert
from OrcApi.OrcDriver.Web.Widget.WidgetButton import WidgetButton
from OrcApi.OrcDriver.Web.Widget.WidgetInput import WidgetInput
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from OrcApi.OrcDriver.Web.Widget.WidgetSelect import WidgetSelect
from OrcLib import LibCommon
from OrcLib import get_config
from OrcLib.LibCmd import WebCmd
from OrcLib.LibLog import OrcLog
from WebDriverService import WebDriverService

LibCommon.set_default_encoding()


class WebDriver:

    def __init__(self):

        # Log
        self._logger = OrcLog("driver.web.selenium")

        # service
        self._service = WebDriverService()

        # configer
        self._driver_configer = get_config("driver")

        # 浏览器
        self._browser = self._driver_configer.get_option('WEB', 'browser')

        # 环境
        self._env = self._driver_configer.get_option('DEFAULT', 'env')

        # 窗口,用于窗口切换
        self._window = None

        # 根节点
        self._root = None

        # 存储出现过的对象
        self._objects = {}

        # 截图
        self._pic_name = self._driver_configer.get_option("WEB", "pic_name")

    def set_env(self, p_env):
        """
        设置环境
        :param p_env:
        :return:
        """
        self._env = p_env
        self._driver_configer.set_option('DEFAULT', 'environment', p_env)

    def execute(self, p_cmd):
        """
        执行调用
        :param p_cmd: {TYPE, PARA, OPERATE}
        :type p_cmd: WebCmd
        :return:
        """
        self._logger.debug("Run WEB command: " % p_cmd.get_cmd_dict())

        if p_cmd.is_page():
            _status = self.__get_page(p_cmd)
        elif p_cmd.is_widget():
            _status = self.__action(p_cmd)
        else:
            self._logger.error("Wrong type %s." % p_cmd.cmd_type)
            return False

        self.save_screen()

        self._logger.debug("Run WEB status is : " % p_cmd.get_cmd_dict())

        return _status

    def __action(self, p_para):
        """
        操作
        :param p_para:
        :type p_para: WebCmd
        :return:
        """
        _definition = self._service.widget_get_definition(p_para.cmd_object)

        # 输入框
        if "INP" == _definition.widget_type:
            _node = WidgetInput(self._root, p_para.cmd_object)
            result = _node.execute(p_para)

        # Button
        elif "BTN" == _definition.widget_type:
            _node = WidgetButton(self._root, p_para.cmd_object)
            result = _node.execute(p_para)

        # <a href>
        elif "A" == _definition.widget_type:
            _node = WidgetA(self._root, p_para.cmd_object)
            result = _node.execute(p_para)

        # 下拉框
        elif "SELECT" == _definition.widget_type:
            _node = WidgetSelect(self._root, p_para.cmd_object)
            result = _node.execute(p_para)

        # win 提示框
        elif 'ALERT' == _definition.widget_type:
            _node = WidgetAlert(self._root)
            result = _node.execute(p_para)

        # 自定义控件
        else:
            _node = WidgetBlock(self._root, p_para.cmd_object)
            result = _node.basic_execute(p_para)

        return result

    def __get_page(self, p_para):
        """
        打开浏览器
        :param p_para: {BROWSER, ID, ENV, OPERATION}
        :type p_para: WebCmd
        :return:
        """
        self._logger.debug(p_para)

        # 浏览器
        self._browser = self._driver_configer.get_option("WEB", "browser")
        if not self._browser:
            self._browser = "PHANTOMJS"

        # 环境
        self._env = self._driver_configer.get_option("WEB", "env")
        if not self._env:
            self._env = "TEST"

        if self._root is None:

            driver_path = self._driver_configer.get_option(self._browser, "path")

            try:
                if "IE" == self._browser:
                    self._root = webdriver.Ie(executable_path=driver_path)

                elif "FIREFOX" == self._browser:
                    self._root = webdriver.Firefox(executable_path=driver_path)

                elif "CHROME" == self._browser:
                    self._root = webdriver.Chrome(executable_path=driver_path)

                elif "PHANTOMJS" == self._browser:
                    self._root = webdriver.PhantomJS(executable_path=driver_path)

                else:
                    self._logger.error("Unsupported browser: %s" % self._browser)

            except WebDriverException:
                self._logger.error("Open browser failed.")
                return False

        if "GET" == p_para.cmd_operation:
            # 设置加载时间,貌似没用
            self._root.set_page_load_timeout(20)

            # 获取 URL
            _url = self._service.page_get_url(self._env, p_para.cmd_object)

            # 打开界面
            try:
                self.get(_url)
            except TimeoutException:
                pass

        elif "MAX" == p_para.cmd_type:
            self._root.maximize_window()

        elif "QUIT" == p_para.cmd_object:
            self._root.quit()

        return self._root is not None

    def get(self, p_url, p_timeout=40):

        def _get(_url, _flag):
            self._root.get(_url)
            _flag.put(True)

        flag = multiprocessing.Queue()
        p = multiprocessing.Process(target=_get, args=(p_url, flag))
        p.start()

        for i in range(p_timeout):
            try:
                if flag.get_nowait():
                    return True
            except queues.Empty:
                pass

            sleep(1)

        return True

    def save_screen(self):

        time.sleep(0.5)

        if self._pic_name is None:
            self._logger.error("get pic name failed")
            return

        self._root.save_screenshot(self._pic_name)
