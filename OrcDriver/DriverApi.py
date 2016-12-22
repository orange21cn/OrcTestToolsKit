# coding=utf-8
from flask_restful import Resource
from flask import send_file

from OrcLib import init_log
from OrcLib import get_config
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_api
from OrcLib.LibNet import OrcParameter
from DriverModel import DriverModel


class DriverAPI(Resource):

    def __init__(self):

        init_log()

        self.__logger = OrcLog("driver.api")
        self.__configer = get_config("driver")
        self.__model = DriverModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def put(self):
        """
        调试
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__model.debug(parameter)

    @orc_api
    def post(self):
        """
        执行
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__model.run(parameter)

    def get(self):
        """
        获取载图
        :return:
        """
        file_name = self.__configer.get_option("WEB", "pic_name")
        return send_file(file_name, mimetype='image/png', cache_timeout=0)
