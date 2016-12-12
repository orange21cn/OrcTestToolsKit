# coding=utf-8
from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api
from DictBus import DictListBus
from DictBus import DictBus


class DictListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.lib.dicts")
        self.__business = DictListBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def post(self):
        """
        新增
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add dict, parameter is: %s" % parameter)

        return self.__business.bus_list_add(parameter)

    @orc_api
    def delete(self):
        """
        删除
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Delete dict, parameter is: %s" % parameter)

        return self.__business.bus_list_delete(parameter)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search dict, parameter is: %s" % parameter)

        return self.__business.bus_list_search(parameter)


class DictAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.lib.dict")
        self.__business = DictBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        self.__logger.info("Delete dict, parameter is: %s" % p_id)

        return self.__business.bus_delete(p_id)

    @orc_api
    def put(self, p_id):
        """
        更新
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Update dict, parameter is: %s, %s" % (p_id, parameter))

        return self.__business.bus_update(p_id, parameter)

    @orc_api
    def get(self, p_id):
        """
        查询
        :param p_id:
        :return:
        """
        self.__logger.info("Search dict, parameter is: %s" % p_id)

        return self.__business.bus_search(p_id)
