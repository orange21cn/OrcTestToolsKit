# coding=utf-8
from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api
from CaseBus import CaseDefBus
from CaseBus import CaseDetBus


class CaseDefListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.cases.api.def")
        self.__business = CaseDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add case, parameter is: %s" % parameter)

        return self.__business.bus_list_add(parameter)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search case, parameter is: %s" % parameter)

        return self.__business.bus_list_search(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Delete case, parameter is: %s" % parameter)

        return self.__business.bus_list_delete(parameter)


class CaseDefAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.case.api.def")
        self.__business = CaseDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        self.__logger.info("Search case, parameter is: %s" % p_id)

        return self.__business.bus_search(p_id)

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Update case, parameter is: %s, %s" % (p_id, parameter))

        return self.__business.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        self.__logger.info("Delete case, parameter is: %s" % p_id)

        return self.__business.bus_delete(p_id)


class CaseDetListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.cases.api.det")
        self.__business = CaseDetBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add case, parameter is: %s" % parameter)

        return self.__business.bus_list_add(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Delete case, parameter is: %s" % parameter)

        return self.__business.bus_list_delete(parameter)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search case, parameter is: %s" % parameter)

        return self.__business.bus_list_search(parameter)


class CaseDetAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.case.api.det")
        self.__business = CaseDetBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        self.__logger.info("Search case, parameter is: %s" % p_id)

        return self.__business.bus_search(p_id)

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search case, parameter is: %s, %s" % (p_id, parameter))

        return self.__business.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        self.__logger.info("Search case, parameter is: %s" % p_id)

        return self.__business.bus_delete(p_id)
