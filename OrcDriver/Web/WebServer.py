# coding=utf-8
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from OrcDriver.Web.Widget.OrcWidget import OrcWidget
from OrcLib.LibLog import OrcLog
from service import DriverService


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
        _node = None

        if "GET_PAGE" == _type:
            _node = self.__get_page(_para)
        elif "GET_WIDGET" == _type:
            _node = OrcWidget(self.__root, _para)
            print _node.exists()
        else:
            self.__logger.error("Wrong type %s." % _type)

        if _node is not None:
            _node = "Success"

        return _node

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

    # def __design(self):
    #
    #     for wid in definition:
    #
    #         for item in wid:
    #
    #             get_object(item)



