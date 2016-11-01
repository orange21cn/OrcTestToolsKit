# coding=utf-8
from flask.ext.restful import Resource
from flask import request

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_get_parameter
from OrcLib.LibNet import OrcResult
from BatchDefModel import BatchDefModel
from BatchDetModel import BatchDetModel


class BatchDefListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.batch.defs")
        self.__model = BatchDefModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request()

    def get(self):
        """
        Search
        :return:
        """
        parameter = orc_get_parameter()
        rtn = OrcResult()

        mode = parameter["type"] if "type" in parameter else None
        batch_id = parameter["id"] if "id" in parameter else None

        # 查询符合条件的整用例树,至根节点
        if "all" == mode:
            value = self.__model.usr_search_all(parameter)

        # 查询用例及子节点
        elif "tree" == mode:
            if not batch_id:
                value = list()
            else:
                value = self.__model.usr_search_tree(batch_id)

        # 查询用例路径
        elif "path" == mode:
            if not batch_id:
                value = list()
            else:
                value = self.__model.usr_search_path(batch_id)

        # 其他情况只查询符合条件的数据
        else:
            value = self.__model.usr_search(parameter)

        rtn.set_data(value)

        return rtn.get_message()

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


class BatchDefAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.batch.def")
        self.__model = BatchDefModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request()

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


class BatchDetListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.batch.dets")
        self.__model = BatchDetModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request()

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


class BatchDetAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.batch.det")
        self.__model = BatchDetModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request()

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