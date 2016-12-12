# coding=utf-8
from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api
from RunDefBus import RunDefBus
from RunDetMod import RunDetMod
from RunCore import RunCore


class RunDefListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.runs.api.def")
        self.__business = RunDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add run, parameter is: %s" % parameter)

        return self.__business.bus_list_add(parameter)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search run, parameter is: %s" % parameter)

        return self.__business.bus_list_search(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Delete run, parameter is: %s" % parameter)

        return self.__business.bus_list_delete(parameter)


class RunDetListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.runs.api.det")
        self.__model = RunDetMod()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add run time, parameter is: %s" % parameter)

        return self.__model.usr_search(parameter)


class RunAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.run.api")
        self.__model = RunCore()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def put(self):
        """
        start
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Run, parameter is: %s" % parameter)

        return self.__model.run_start(parameter)
