# coding=utf-8
from PySide.QtGui import QSizePolicy

from OrcLib import get_config
from OrcView.Lib.LibView import SelectDictionary
from OrcView.Lib.LibMain import LogClient


class RunEnv(SelectDictionary):

    def __init__(self):

        SelectDictionary.__init__(self, 'test_env')

        self.__logger = LogClient()

        self.get_env()

        self.currentIndexChanged.connect(self.set_env)

        # 设置在拉伸方式
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def set_env(self, p_index):
        """
        设置环境
        :param p_index:
        :return:
        """
        configer = get_config('driver')
        env_data = self.get_data()

        configer.set_option('WEB', 'env', env_data)

    def get_env(self):
        """
        从配置文件中获取当前环境并显示到控件上
        :return:
        """
        configer = get_config('driver')
        env_data = configer.get_option('WEB', 'env')

        self.set_data(env_data)


class RunBrowser(SelectDictionary):

    def __init__(self):

        SelectDictionary.__init__(self, 'browser')

        self.__logger = LogClient()

        self.get_browser()

        self.currentIndexChanged.connect(self.set_browser)

        # 设置在拉伸方式
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def set_browser(self, p_index):
        """
        设置环境
        :param p_index:
        :return:
        """
        configer = get_config('driver')
        browser = self.get_data()

        configer.set_option('WEB', 'browser', browser)

    def get_browser(self):
        """
        从配置文件中获取当前环境并显示到控件上
        :return:
        """
        configer = get_config('driver')
        browser = configer.get_option('WEB', 'browser')

        self.set_data(browser)
