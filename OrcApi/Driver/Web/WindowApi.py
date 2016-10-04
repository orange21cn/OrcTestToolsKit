from flask.ext.restful import Resource
from flask import request

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_get_parameter
from OrcLib.LibNet import OrcReturn
from WindowDefModel import WindowDefModel


class WindowsListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.driver.web.windows")
        self.__model = WindowDefModel()

    def dispatch_request(self, *args, **kwargs):

        _method = getattr(self, request.method.lower(), None)

        if _method is None and request.method == 'HEAD':
            _method = getattr(self, 'get', None)

        return _method(*args, **kwargs)

    def get(self):
        return 1


class WindowsAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.driver.web.window")
        self.__model = WindowDefModel()

    def dispatch_request(self, *args, **kwargs):

        _method = getattr(self, request.method.lower(), None)

        if _method is None and request.method == 'HEAD':
            _method = getattr(self, 'get', None)

        return _method(*args, **kwargs)

    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        _parameter = dict(id=p_id)
        _return = OrcReturn()

        _value = self.__model.usr_search(_parameter)

        _return.set_db_result(_value)

        return _return.get_return()

    def post(self, p_id):
        """
        Add
        :param p_id:
        :return:
        """
        # Todo
        _parameter = dict(id=p_id)
        _return = OrcReturn()

        _value = self.__model.usr_search(_parameter)

        _return.set_db_result(_value)

        return _return.get_return()

    def put(self, p_id):
        """
        Update
        :param id:
        :return:
        """
        _parameter = dict(id=p_id)
        _return = OrcReturn()

        _value = self.__model.usr_search(_parameter)

        _return.set_db_result(_value)

        return _return.get_return()

    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        _parameter = dict(id=p_id)
        _return = OrcReturn()

        _value = self.__model.usr_search(_parameter)

        _return.set_db_result(_value)

        return _return.get_return()

