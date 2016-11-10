# coding=utf-8
from DriverService import WebDriverService


class DriverModel:
    """
    实现驱动分配
    """
    def __init__(self):

        self.__service = WebDriverService()

    def run(self, p_cmd):
        """
        执行步骤
        :param p_cmd:
        :return:
        """
        return self.__service.run(p_cmd)

    def get_status(self):
        """
        获取执行完成列表
        :return:
        """
        return 1

    def debug(self, p_cmd):
        """
        调试
        :param p_cmd:
        :return:
        """
        self.__service.run(p_cmd)
