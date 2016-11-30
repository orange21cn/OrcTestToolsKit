# coding=utf-8
from flask_restful import Resource

from OrcLib import init_log
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_get_parameter
from OrcLib.LibNet import OrcResult
from DriverModel import DriverModel


class DriverAPI(Resource):

    def __init__(self):

        init_log()

        self.__logger = OrcLog("driver.api")
        self.__model = DriverModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def put(self):
        """
        调试
        :return:
        """
        parameter = orc_get_parameter()
        rtn = OrcResult()

        value = self.__model.debug(parameter)

        rtn.set_data(value)

        return rtn.rtn()

    def post(self):
        """
        执行
        :return:
        """
        parameter = orc_get_parameter()

        self.__logger.debug("input parameter: %s" % parameter)

        rtn = OrcResult()

        value = self.__model.run(parameter)

        rtn.set_data(value)

        self.__logger.debug("result: %s" % rtn.rtn())

        return rtn.rtn()

    def get(self):
        """
        获取结果
        :return:
        """
        _return = OrcResult()

        _value = self.__model.get_status()

        _return.set_data(_value)

        return _return.rtn()
