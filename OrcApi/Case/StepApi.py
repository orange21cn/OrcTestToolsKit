from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api
from StepBus import StepDefBus
from StepBus import StepDetBus


class StepDefListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.steps.api.def")
        self.__model = StepDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request()

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add step, parameter is: %s" % parameter)

        return self.__model.bus_list_add(parameter)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search step, parameter is: %s" % parameter)

        return self.__model.bus_list_search(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Delete step, parameter is: %s" % parameter)

        return self.__model.bus_list_delete(parameter)


class StepDefAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.step.api.def")
        self.__model = StepDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        self.__logger.info("Search step, parameter is: %s" % p_id)

        return self.__model.bus_search(p_id)

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Update step, parameter is: %s, %s" % (p_id, parameter))

        return self.__model.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        self.__logger.info("Delete step, parameter is: %s" % p_id)

        return self.__model.bus_delete(p_id)


class StepDetListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.steps.api.det")
        self.__business = StepDetBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add step, parameter is: %s" % parameter)

        return self.__business.bus_list_add(parameter)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search step, parameter is: %s" % parameter)

        return self.__business.bus_list_search(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Delete step, parameter is: %s" % parameter)

        return self.__business.bus_delete(parameter)


class StepDetAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.step.api.det")
        self.__business = StepDetBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        self.__logger.info("Search step, parameter is: %s" % p_id)

        return self.__business.bus_search(p_id)

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Update step, parameter is: %s, %s" % (p_id, parameter))

        return self.__business.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        self.__logger.info("Delete step, parameter is: %s" % p_id)

        return self.__business.bus_delete(p_id)
