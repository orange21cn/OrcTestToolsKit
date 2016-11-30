from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api
from ItemBus import ItemBus


class ItemListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.items")
        self.__business = ItemBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_add(parameter)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_search(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_delete(parameter)


class ItemAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.item")
        self.__business = ItemBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        return self.__business.bus_list_search(dict(id=p_id))

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_cond:
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()
        _value = self.__business.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        return self.__business.bus_delete(dict(id=p_id))
