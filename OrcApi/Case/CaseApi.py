# coding=utf-8
from flask.ext.restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_get_parameter
from OrcLib.LibNet import OrcResult
from CaseDefModel import CaseDefModel
from CaseDetModel import CaseDetModel


class CaseDefListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.case.defs")
        self.__model = CaseDefModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def get(self):
        """
        Search
        :return:
        """
        parameter = orc_get_parameter()
        rtn = OrcResult()

        mode = parameter["type"] if "type" in parameter else None
        case_id = parameter["id"] if "id" in parameter else None

        # 查询符合条件的整用例树,至根节点
        if "all" == mode:
            value = self.__model.usr_search_all(parameter)

        # 查询用例及子节点
        elif "tree" == mode:
            if not case_id:
                value = list()
            else:
                value = self.__model.usr_search_tree(case_id)

        # 查询用例路径
        elif "path" == mode and case_id:
            if not case_id:
                value = list()
            else:
                value = self.__model.usr_search_path(case_id)

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


class CaseDefAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.case.def")
        self.__model = CaseDefModel()

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


class CaseDetListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.case.dets")
        self.__model = CaseDetModel()

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


class CaseDetAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.case.det")
        self.__model = CaseDetModel()

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
