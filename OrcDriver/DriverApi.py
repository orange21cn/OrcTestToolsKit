# coding=utf-8
from flask.ext.restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_get_parameter
from OrcLib.LibNet import OrcResult
from DriverModel import DriverModel


class DriverAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.run.defs")
        self.__model = DriverModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request()

    def post(self):
        """
        Search
        :return:
        """
        parameter = orc_get_parameter()
        rtn = OrcResult()

        value = self.__model.run(parameter)

        rtn.set_data(value)

        return rtn.get_message()

    def get(self):
        """
        Delete
        :return:
        """
        _return = OrcResult()

        _value = self.__model.get_status()

        _return.set_data(_value)

        return _return.get_message()