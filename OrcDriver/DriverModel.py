# coding=utf-8
from DriverService import WebDriverService


class DriverModel:
    """
    实现驱动分配
    """
    def __init__(self):

        self.__service = WebDriverService()

    def run(self, p_cmd):
        return self.__service.run(p_cmd)

    def get_status(self):
        return