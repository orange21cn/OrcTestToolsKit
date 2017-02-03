# coding=utf-8
from flask_restful import Resource

from OrcLib import init_log
from OrcLib.LibNet import orc_api
from OrcLib.LibNet import OrcLog
from OrcLib.LibNet import OrcParameter
from OrcLib.LibException import OrcApiModelFailException


class OrcBaseAPI(Resource):

    def __init__(self, p_flag, p_bus):

        self._flag = p_flag
        self._business = p_bus()
        self._logger = OrcLog("resource.%s.api" % self._flag)

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)


class OrcStatusAPI(Resource):

    def __init__(self, p_flag, p_bus):

        self._flag = p_flag
        self._business = p_bus()
        self._logger = OrcLog("resource.%s.api" % self._flag)

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self):
        return True


class OrcListAPI(OrcBaseAPI):

    def __init__(self, p_flag, p_bus):

        OrcBaseAPI.__init__(self, p_flag, p_bus)

        self._logger = OrcLog("resource.%ss.api" % self._flag)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcBaseAPI, self).dispatch_request(*args, **kwargs)

    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.api_get(parameter)

    @orc_api
    def api_get(self, p_para):

        self._logger.info("Search %s, parameter is: %s" % (self._flag, p_para))
        return self._business.bus_list_search(p_para)

    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.api_post(parameter)

    @orc_api
    def api_post(self, p_para):
        """
        Add
        :param p_para:
        :return:
        """
        self._logger.info("Add %s, parameter is: %s" % (self._flag, p_para))

        return self._business.bus_list_add(p_para)

    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.api_delete(parameter)

    @orc_api
    def api_delete(self, p_para):
        """
        Delete
        :param p_para:
        :return:
        """
        self._logger.info("Delete %s, parameter is: %s" % (self._flag, p_para))

        return self._business.bus_list_delete(p_para)


class OrcAPI(OrcBaseAPI):

    def __init__(self, p_flag, p_bus):

        OrcBaseAPI.__init__(self, p_flag, p_bus)

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        return self.api_get(p_id)

    @orc_api
    def api_get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        self._logger.info("Search %s, parameter is: %s" % (self._flag, p_id))

        return self._business.bus_search(p_id)

    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.api_put(p_id, parameter)

    @orc_api
    def api_put(self, p_id, p_para):
        """
        Update
        :param p_para:
        :param p_id:
        :return:
        """
        self._logger.info("Update %s, parameter is: %s, %s" % (self._flag, p_id, p_para))

        return self._business.bus_update(p_id, p_para)

    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        return self.api_delete(p_id)

    @orc_api
    def api_delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        self._logger.info("Delete %s, parameter is: %s" % (self._flag, p_id))

        return self._business.bus_delete(p_id)


class OrcBus(object):

    def __init__(self, p_flag, p_model):

        object.__init__(self)

        init_log()

        self._flag = p_flag
        self._model = p_model()
        self._logger = OrcLog("resource.%s.bus" % self._flag)

    def bus_list_add(self, p_cond):
        """
        新增
        :param p_cond:
        :return:
        """
        try:
            result = self._model.usr_add(p_cond)
        except Exception:
            self._logger.error("Add %s error, input: %s" % (self._flag, p_cond))
            raise OrcApiModelFailException

        return result

    def bus_list_delete(self, p_list):
        """
        删除 list, 调用单个删除函数
        :param p_list:
        :return:
        """
        try:
            for _id in p_list:
                self.bus_delete(_id)
        except Exception:
            self._logger.error("Delete %s error, input: %s" % (self._flag, p_list))
            raise OrcApiModelFailException

        return True

    def bus_list_search(self, p_cond):
        """
        查询 list
        :param p_cond:
        :return:
        """
        try:
            result = self._model.usr_search(p_cond)
        except Exception:
            self._logger.error("Search %s error, input: %s" % (self._flag, p_cond))
            raise OrcApiModelFailException

        return result

    def bus_update(self, p_id, p_cond):
        """
        更新一条
        :param p_id:
        :param p_cond:
        :return:
        """
        cond = p_cond
        cond["id"] = p_id

        try:
            self._model.usr_update(cond)
        except Exception:
            self._logger.error("Update %s error, input: %s" % (self._flag, p_cond))
            raise OrcApiModelFailException

        return True

    def bus_delete(self, p_id):
        """
        删除一条
        :param p_id:
        :return:
        """
        try:
            self._model.usr_delete(p_id)
        except Exception:
            self._logger.error("Delete %s error, input: %s" % (self._flag, p_id))
            raise OrcApiModelFailException

        return True

    def bus_search(self, p_id):
        """
        查询一条
        :param p_id:
        :return:
        """
        try:
            result = self._model.usr_search(dict(id=p_id))
            result = None if not result else result[0]
        except Exception:
            self._logger.error("Search %s error, input: %s" % (self._flag, p_id))
            raise OrcApiModelFailException

        return result


def connect_list(p_lists, p_detail, p_flag):
    """
    连接两个数组
    :param p_lists: list 1
    :type p_lists: list
    :param p_detail: list 2
    :type p_detail: list
    :param p_flag: 标志字段
    :type p_flag: str
    :return:
    :rtype: list
    """
    result = []

    if not p_detail:
        return result

    for _item in p_lists:

        _item.pop("create_time")

        for _det in p_detail:

            if _det["id"] == _item[p_flag]:

                temp = _det.copy()
                temp.pop("id")

                _item.update(temp)

                break

        result.append(_item)

    return result
