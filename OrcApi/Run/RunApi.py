# coding=utf-8
from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_get_parameter
from OrcLib.LibNet import OrcResult
from RunDefModel import RunDefModel
from RunDetModel import RunDetModel
from RunCore import RunCore


class RunDefListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.run.defs")
        self.__model = RunDefModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def get(self):
        """
        Search
        :return:
        """
        parameter = orc_get_parameter()
        rtn = OrcResult()

        value = self.__model.usr_search(parameter)

        rtn.set_data(value)

        return rtn.rtn()

    def delete(self):
        """
        Delete
        :return:
        """
        _parameter = orc_get_parameter()
        _return = OrcResult()

        delete_list = _parameter["list"]
        _value = self.__model.usr_delete(delete_list)

        _return.set_data(_value)

        return _return.rtn()


class RunDefAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.run.def")
        self.__model = RunDefModel()

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

        return _return.rtn()

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

        return _return.rtn()

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

        return _return.rtn()


class RunDetListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.case.dets")
        self.__model = RunDetModel()

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

        return _return.rtn()


class RunAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.case.dets")
        self.__model = RunCore()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def get(self):
        """
        get status
        :return:
        """
        _return = OrcResult()

        _value = self.__model.run_get_status()

        _return.set_data(_value)

        return _return.rtn()

    def put(self):
        """
        start
        """
        _return = OrcResult()
        _parameter = orc_get_parameter()

        self.__model.run_start(_parameter)

        return _return.rtn()

    def post(self):
        """
        DEBUG
        """
        pass
