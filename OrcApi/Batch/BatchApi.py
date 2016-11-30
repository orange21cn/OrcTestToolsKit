# coding=utf-8
from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api
from BatchBus import BatchDefBus
from BatchBus import BatchDetBus


class BatchDefListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.batch.api.defs")
        self.__business = BatchDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_search(parameter)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_add(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_delete(parameter)


class BatchDefAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.batch.def")
        self.__model = BatchDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        return self.__model.bus_search(p_id)

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__model.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        return self.__model.bus_delete(p_id)


class BatchDetListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.batch.dets")
        self.__business = BatchDetBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_search(parameter)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()
        return dict(id=self.__business.bus_list_add(parameter))

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_delete(parameter)


class BatchDetAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.batch.det")
        self.__business = BatchDetBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        parameter = dict(id=p_id)
        return self.__business.bus_search(parameter)

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        return self.__business.bus_delete(p_id)
