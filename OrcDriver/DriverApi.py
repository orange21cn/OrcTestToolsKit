# coding=utf-8
from flask_restful import Resource

from OrcLib import init_log
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_api
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import OrcResult
from DriverModel import DriverModel


class DriverAPI(Resource):

    def __init__(self):

        init_log()

        self.__logger = OrcLog("driver.api")
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

    @orc_api
    def get(self):
        """
        获取结果
        :return:
        """
        pass
