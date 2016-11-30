from flask_restful import Resource
from flask import request

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcParameter

from WindowBus import WindowDefBus


class WindowListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.driver.web.windows")
        self.__business = WindowDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request()

    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_add(parameter)

    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_delete(parameter)

    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_list_search(parameter)


class WindowAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.driver.web.window")
        self.__business = WindowDefBus()

    def dispatch_request(self, *args, **kwargs):

        _method = getattr(self, request.method.lower(), None)

        if _method is None and request.method == 'HEAD':
            _method = getattr(self, 'get', None)

        return _method(*args, **kwargs)

    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        return self.__business.bus_delete(p_id)

    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.__business.bus_update(p_id, parameter)

    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        return self.__business.bus_search(p_id)
