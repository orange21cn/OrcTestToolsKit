# coding=utf-8
from flask_restful import Resource
from flask import send_file

from OrcLib import get_config
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_api
from OrcLib.LibNet import OrcParameter
from DriverModel import DriverModel


class DriverListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("driver.api")
        self.__configer = get_config("driver")
        self.__model = DriverModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def put(self):
        """
        调试
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.api_put(parameter)

    @orc_api
    def api_put(self, p_para):
        return self.__model.debug(p_para)

    def post(self):
        """
        执行
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.api_post(parameter)

    @orc_api
    def api_post(self, p_para):
        return self.__model.run(p_para)

    def get(self):
        """
        获取载图
        :return:
        """
        file_name = self.__configer.get_option("WEB", "pic_name")
        return self.api_get(file_name)

    @staticmethod
    def api_get(p_file):
        return send_file(p_file, mimetype='image/png', cache_timeout=0)


# GET /pic
# GET /DriverMessage
# GET /DriverStatus
# GET /RunStatus
# POST /Run
# PUt /ID/START
# PUT /ID/STOP
