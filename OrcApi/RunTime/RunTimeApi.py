# coding=utf-8
from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api
from RunTimeBus import RunTimeBus


class RunTimeListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.run_times.api.def")
        self.__business = RunTimeBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search run_times, parameter is: %s" % parameter)

        return self.__business.bus_list_search(parameter)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add run_times, parameter is: %s" % parameter)

        return self.__business.bus_list_add(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Delete run_times, parameter is: %s" % parameter)

        return self.__business.bus_list_delete(parameter)


class RunTimeAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.run_times.api.def")
        self.__model = RunTimeBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        self.__logger.info("Search run_times, parameter is: %s" % p_id)

        return self.__model.bus_search(p_id)

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Update run_times, parameter is: %s, %s" % (p_id, parameter))

        return self.__model.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        self.__logger.info("Delete run_times, parameter is: %s" % p_id)

        return self.__model.bus_delete(p_id)
