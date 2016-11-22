from flask.ext.restful import Resource
from flask import request

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_get_parameter
from OrcLib.LibNet import OrcResult
from PageDefModel import PageDefModel
from PageDetModel import PageDetModel


class PageDefListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.page.defs")
        self.__model = PageDefModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def get(self):
        """
        Search
        :return:
        """
        _parameter = orc_get_parameter()
        _return = OrcResult()

        _value = self.__model.usr_search(_parameter)

        _return.set_data(_value)

        return _return.get_message()

    def delete(self):
        """
        Delete
        :return:
        """
        _parameter = orc_get_parameter()
        _return = OrcResult()

        _value = self.__model.usr_delete(_parameter)

        _return.set_data(_value)

        return _return.get_message()


class PageDefAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.page.def")
        self.__model = PageDefModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        _parameter = dict(id=p_id)
        _return = OrcResult()

        _value = self.__model.usr_search(_parameter)

        if _value:
            _return.set_data(_value[0])
        else:
            _return.set_data(None)

        return _return.get_message()

    def post(self, p_id):
        """
        Add
        :param p_id:
        :return:
        """
        _parameter = orc_get_parameter()
        _parameter["id"] = p_id
        _return = OrcResult()

        _value = self.__model.usr_add(_parameter)

        _return.set_data(str(_value))

        return _return.get_message()

    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        _parameter = orc_get_parameter()
        _parameter["id"] = p_id
        _return = OrcResult()

        _value = self.__model.usr_update(_parameter)

        _return.set_data(_value)

        return _return.get_message()

    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        _parameter = p_id
        _return = OrcResult()

        _value = self.__model.usr_delete(_parameter)

        _return.set_data(_value)

        return _return.get_message()


class PageDetListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.page.dets")
        self.__model = PageDetModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def get(self):
        """
        Search
        :return:
        """
        _parameter = orc_get_parameter()
        _return = OrcResult()

        _value = self.__model.usr_search(_parameter)

        _return.set_data(_value)

        return _return.get_message()

    def delete(self):
        """
        Delete
        :return:
        """
        _parameter = orc_get_parameter()
        _return = OrcResult()

        _value = self.__model.usr_delete(_parameter)

        _return.set_data(_value)

        return _return.get_message()


class PageDetAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.page.det")
        self.__model = PageDetModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        _parameter = dict(id=p_id)
        _return = OrcResult()

        _value = self.__model.usr_search(_parameter)

        if _value:
            _return.set_data(_value[0])
        else:
            _return.set_data(None)

        return _return.get_message()

    def post(self, p_id):
        """
        Add
        :param p_id:
        :return:
        """
        _parameter = orc_get_parameter()
        _parameter["id"] = p_id
        _return = OrcResult()

        _value = self.__model.usr_add(_parameter)

        _return.set_data(str(_value))

        return _return.get_message()

    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        _parameter = orc_get_parameter()
        _parameter["id"] = p_id
        _return = OrcResult()

        _value = self.__model.usr_update(_parameter)

        _return.set_data(_value)

        return _return.get_message()

    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        _parameter = p_id
        _return = OrcResult()

        _value = self.__model.usr_delete(_parameter)

        _return.set_data(_value)

        return _return.get_message()