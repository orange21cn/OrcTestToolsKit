# coding=utf-8
import sys
import json
import socket
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException

from OrcLib import LibCommon
from OrcLib.LibLog import OrcLog
from OrcLib import get_config
from OrcDriver.Web.Widget.OrcWidget import WidgetBlock
from OrcDriver.Web.Widget.WidgetButton import WidgetButton
from OrcDriver.Web.Widget.WidgetInput import WidgetInput
from OrcDriver.Web.Widget.WidgetA import WidgetA
from OrcDriver.Web.Widget.WidgetSelect import WidgetSelect
from OrcDriver.Web.Widget.WidgetAlert import WidgetAlert

from WebDriverService import WebDriverService

LibCommon.set_default_encoding()


class DriverSelenium:

    def __init__(self, p_ip, p_port):

        self.__logger = OrcLog("driver.web.selenium")
        self.__service = WebDriverService()
        self.__driver_configer = get_config("driver")

        # 浏览器
        self.__browser = self.__driver_configer.get_option('WEB', 'browser')

        # 环境
        self.__env = self.__driver_configer.get_option('WEB', 'env')

        # 窗口,用于窗口切换
        self.__window = None

        # 根节点
        self.__root = None

        # 存储出现过的对象
        self.__objects = {}

        # IP
        self.__ip = p_ip

        # port
        self.__port = int(p_port)

        # 截图
        self.__pic_name = self.__driver_configer.get_option("WEB", "pic_name")

    def start(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.__ip, self.__port))
        sock.listen(1)

        while True:

            connection, address = sock.accept()

            try:
                connection.settimeout(5)

                _cmd = json.loads(connection.recv(1024))

                self.__logger.info("Run command %s" % _cmd)

                if ("quit" in _cmd) and ("QUIT" == _cmd["quit"]):
                    if self.__root is not None:
                        self.__root.quit()
                    break

                _result = self.__execute(_cmd)

                connection.send(str(_result))

            except socket.timeout:
                self.__logger.error("time out")
                connection.send(str(False))

            except Exception, err:
                self.__logger.error(err)
                connection.send(str(False))

            connection.close()

    def __execute(self, p_cmd):
        """
        执行调用
        :param p_cmd: {TYPE, PARA, OPERATE}
        :return:
        """
        self.__logger.debug("Run WEB command: " % p_cmd)

        _type = p_cmd["TYPE"]

        if "PAGE" == _type:
            _status = self.__get_page(p_cmd)

        elif "WIDGET" == _type:
            _status = self.__action(p_cmd)

        else:
            self.__logger.error("Wrong type %s." % _type)
            return False

        self.save_screen()

        self.__logger.debug("Run WEB status is : " % p_cmd)

        return _status

    def __action(self, p_para):

        _id = p_para["OBJECT"]
        _definition = self.__service.widget_get_definition(_id)

        # 输入框
        if "INP" == _definition.widget_type:
            _node = WidgetInput(self.__root, _id)
            result = _node.execute(p_para)

        # Button
        elif "BTN" == _definition.widget_type:
            _node = WidgetButton(self.__root, _id)
            result = _node.execute(p_para)

        # <a href>
        elif "A" == _definition.widget_type:
            _node = WidgetA(self.__root, _id)
            result = _node.execute(p_para)
            print "===", result

        # 下拉框
        elif "SELECT" == _definition.widget_type:
            _node = WidgetSelect(self.__root, _id)
            result = _node.execute(p_para)

        # win 提示框
        elif 'ALERT' == _definition.widget_type:
            _node = WidgetAlert(self.__root)
            result = _node.execute(p_para)

        # 自定义控件
        else:
            _node = WidgetBlock(self.__root, _id)
            result = _node.basic_execute(p_para)
            print "''''''", result

        return result

    def __get_page(self, p_para):
        """
        打开浏览器
        :param p_para: {BROWSER, ID, ENV, OPERATION}
        :return:
        """
        self.__logger.debug(p_para)

        # 浏览器
        self.__browser = self.__driver_configer.get_option("WEB", "browser")
        if not self.__browser:
            self.__browser = "PHANTOMJS"

        # 环境
        self.__env = self.__driver_configer.get_option("WEB", "env")
        if not self.__env:
            self.__env = "TEST"

        _page_det_id = p_para["OBJECT"]
        _page_operation = p_para["OPERATION"]

        if self.__root is None:

            driver_path = self.__driver_configer.get_option(self.__browser, "path")

            try:
                if "IE" == self.__browser:
                    self.__root = webdriver.Ie(executable_path=driver_path)

                elif "FIREFOX" == self.__browser:
                    print driver_path
                    self.__root = webdriver.Firefox(executable_path=driver_path)

                elif "CHROME" == self.__browser:
                    self.__root = webdriver.Chrome(executable_path=driver_path)

                elif "PHANTOMJS" == self.__browser:
                    self.__root = webdriver.PhantomJS(executable_path=driver_path)

                else:
                    self.__logger.error("Unsupported browser: %s" % self.__browser)

            except WebDriverException:
                self.__logger.error("Open browser failed.")
                return False

        if "GET" == _page_operation:
            # 设置加载时间
            self.__root.set_page_load_timeout(10)

            # 获取 URL
            _url = self.__service.page_get_url(self.__env, _page_det_id)

            # 打开界面
            try:
                self.__root.get(_url)
            except TimeoutException:
                pass

        elif "MAX" == _page_operation:
            self.__root.maximize_window()

        elif "QUIT" == _page_operation:
            self.__root.quit()

        return self.__root is not None

    def save_screen(self):

        time.sleep(0.5)

        if self.__pic_name is None:
            self.__logger.error("get pic name failed")
            return

        self.__root.save_screenshot(self.__pic_name)