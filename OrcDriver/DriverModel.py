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
        result = self.__service.run(p_cmd)
        print "-->", result
        return result

    def debug(self, p_cmd):
        """
        调试
        :param p_cmd:
        :return:
        """
        self.__service.run(p_cmd)
