# coding=utf-8
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from OrcLib.LibLog import OrcLog
from service import DriverService

from OrcDriver.Web.Widget.WidgetInput import WidgetInput
from OrcDriver.Web.Widget.WidgetButton import WidgetButton


class DriverSelenium:

    def __init__(self):

        self.__logger = OrcLog("driver.selenium")
        self.__service = DriverService()

        self.__browser = "FIREFOX"  # 浏览器
        self.__env = "TEST"  # 环境

        self.__window = None  # 当前窗口
        self.__root = None  # 根节点

        self.__objects = {}  # 存储出现过的对象

    def execute(self, p_data):
        """
        执行调用
        :param p_data: {TYPE, PARA, OPERATE}
        :return:
        """
        self.__logger.debug(p_data)

        _type = p_data["TYPE"]
        _para = p_data["PARA"]

        if "OPEN_PAGE" == _type:
            _status = self.__get_page(_para)
        elif "EXEC_STEP" == _type:
            _status = self.__action(_para)
        else:
            _status = False
            self.__logger.error("Wrong type %s." % _type)

        return _status

    def __action(self, p_para):

        _id = p_para["ID"]
        _act = p_para["ACTION"]
        _node = None

        _definition = self.__service.widget_get_definition(_id)

        # 输入框
        if "INP" == _definition.widget_type:
            _node = WidgetInput(self.__root, _id)
            _node.execute(_act)

        # Button
        elif "BTN" == _definition.widget_type:
            _node = WidgetButton(self.__root, _id)
            _node.execute(_act)

        # 自定义控件
        else:
            pass

        return True

    def __get_page(self, p_para):
        """
        打开浏览器
        :param p_para: {BROWSER, ID, ENV}
        :return:
        """
        self.__logger.debug(p_para)

        self.__browser = p_para["BROWSER"]
        self.__env = p_para["ENV"]
        _page_id = p_para["ID"]

        # 获取 url
        _url = self.__service.page_get_url(_page_id)

        # 打开页面
        if self.__root is None:

            try:

                if "IE" == self.__browser:
                    self.__root = webdriver.Ie()
                elif "FIREFOX" == self.__browser:
                    self.__root = webdriver.Firefox()
                elif "CHROME" == self.__browser:
                    self.__root = webdriver.Chrome()
                else:
                    pass

                self.__root.get(_url)

            except WebDriverException:
                self.__logger.error("Open browser failed.")

        return self.__root is not None

    def save_screen(self, p_file):
        time.sleep(0.5)
        self.__root.save_screenshot(p_file)




