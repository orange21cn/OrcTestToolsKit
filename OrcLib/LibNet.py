# coding=utf-8
import json
import requests
import subprocess
import socket
from exceptions import ValueError
from functools import wraps
from flask import make_response
from flask import request
from requests.exceptions import RequestException
from requests.packages.urllib3.exceptions import HTTPError
from OrcLib.LibCommon import is_false
from OrcLib.LibLog import OrcLog
from OrcApi import orc_db

_logger = OrcLog("api.test01")


class OrcReturn:
    """
    To be deleted
    """

    def __init__(self):

        self.__result = dict(STATUS="TRUE", VALUE=None)

    def set_status(self, p_res):

        if p_res:
            self.__result["STATUS"] = "TRUE"
        else:
            self.__result["STATUS"] = "FALSE"

    def set_db_result(self, p_values):

        if p_values is None:
            self.__result["VALUE"] = None
        else:
            self.__result["VALUE"] = []
            for t_data in p_values:
                self.__result["VALUE"].append(t_data.to_json())

    def set_str_result(self, p_value):

        if p_value is None:
            self.__result["VALUE"] = None
        else:
            self.__result["VALUE"] = p_value

    def set_arr_result(self, p_value):

        self.__result["VALUE"] = []

        if p_value is not None:
            self.__result["VALUE"].extend(p_value)

    def get_return(self):
        return json.dumps(self.__result)


def orc_invoke(p_url, p_para=""):
    """
    post interface To be deleted
    :param p_url:
    :param p_para:
    :return:
    """
    _type = {'content-type': 'application/json'}
    _para = json.dumps(p_para)
    _result = None

    try:
        _response = requests.post(p_url, data=_para, headers=_type)

        if not _response.ok:
            _logger.error("Invoke %s failed, parameter is %s, response is %s" % (p_url, _para, _response.ok))
            return None

        _result = json.loads(_response.text)

        # 成功返回但结果为 False
        if is_false(_result["STATUS"]):
            _logger.error("Invoke %s failed, parameter is %s, status is %s" % (p_url, _para, _result["STATUS"]))
            return None

    except (HTTPError, ValueError, RequestException):
        # _logger.error("Invoke %s failed, parameter is %s, status is %s" % (p_url, _para, _result["STATUS"]))
        return None

    return _result["VALUE"]


def orc_get_parameter():
    """
    Get parameter for post interface
    :return:
    """
    _rtn = request.json
    if _rtn is None:
        _rtn = dict()
    return _rtn


def allow_cross_domain(fun):
    """
    For javascript post
    :param fun:
    :return:
    """

    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))

        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        rst.headers['Access-Control-Allow-Headers'] = "Referer,Accept,Origin,User-Agent"

        return rst

    return wrapper_fun


class OrcInvoke:
    """
    post interface
    :param p_url:
    :param p_para:
    :return:
    """

    def __init__(self):
        pass

    def get(self, p_url, p_para=None):

        return self.__invoke("GET", p_url, p_para)

    def post(self, p_url, p_para=None):
        """
        :rtype: list
        :param p_para:
        :param p_url:
        """
        return self.__invoke("POST", p_url, p_para)

    def put(self, p_url, p_para=None):

        return self.__invoke("PUT", p_url, p_para)

    def delete(self, p_url, p_para=None):

        return self.__invoke("DELETE", p_url, p_para)

    @staticmethod
    def socket(p_ip, p_port, p_para):
        """
        :param p_para:
        :param p_ip:
        :type p_ip: str
        :param p_port:
        :type p_port: int
        :return:
        """
        import time

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((p_ip, p_port))

        time.sleep(2)
        sock.send(json.dumps(p_para))
        _msg = sock.recv(1024)
        sock.close()

        return _msg

    @staticmethod
    def __invoke(p_flg, p_url, p_para):

        _type = {'content-type': 'application/json'}
        _para = json.dumps(p_para)
        _result = None

        try:
            # 接口调用
            if "GET" == p_flg:
                _response = requests.get(p_url, data=_para, headers=_type)
            elif "POST" == p_flg:
                _response = requests.post(p_url, data=_para, headers=_type)
            elif "PUT" == p_flg:
                _response = requests.put(p_url, data=_para, headers=_type)
            elif "DELETE" == p_flg:
                _response = requests.delete(p_url, data=_para, headers=_type)
            else:
                _response = requests.get(p_url, data=_para, headers=_type)

            # 调用失败
            if not _response.ok:
                _logger.error("Invoke %s failed, parameter is %s, response is %s" % (p_url, _para, _response.ok))
                return None

            _result = OrcResult(_response.text)

            # 成功返回但结果为 False
            if not _result.status:
                _logger.error("Invoke %s failed, parameter is %s, status is %s" % (p_url, _para, _result.status))
                return None

        except (HTTPError, ValueError, RequestException):
            _logger.error("Invoke %s failed, parameter is %s, status is %s" % (p_url, _para, _result.status))
            return None

        return _result.data


class OrcResult:
    def __init__(self, p_res=None):

        self.status = True
        self.data = None

        if p_res is not None:
            _res = json.loads(p_res)
            self.status = _res["STATUS"]
            self.data = _res["DATA"]

    def set_status(self, p_status):
        """
        返回状态
        :param p_status:
        :return:
        """
        self.status = bool(p_status)

    def set_data(self, p_data):
        """
        返回数据
        :param p_data:
        :return:
        """
        if isinstance(p_data, list) \
                and 0 < len(p_data) \
                and isinstance(p_data[0], orc_db.Model):

            self.data = []
            for t_data in p_data:
                self.data.append(t_data.to_json())
        else:
            self.data = p_data

    def get_message(self):
        """
        返回信息字符串
        :return:
        """
        _result = dict(STATUS=self.status,
                       DATA=self.data)
        return _result
