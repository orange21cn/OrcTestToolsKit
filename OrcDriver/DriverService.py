# coding=utf-8
from OrcLib.LibNet import OrcSocketResource


class WebDriverService:

    def __init__(self):

        self.__resource_socket = OrcSocketResource("DriverWeb")

    def run(self, p_cmd):
        """
        执行
        :param p_cmd:
        :return:
        """
        import json
        return self.__resource_socket.get(p_cmd)
