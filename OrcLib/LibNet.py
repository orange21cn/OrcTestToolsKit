# coding=utf-8
import json
import requests

from exceptions import ValueError
from functools import wraps
from flask import make_response
from flask import request
from requests.exceptions import RequestException
from requests.packages.urllib3.exceptions import HTTPError

from OrcLib.LibException import OrcPostFailedException
from OrcLib.LibCommon import is_false

from OrcLib.LibLog import OrcLog


_logger = OrcLog("basic.net")


class OrcReturn:

    def __init__(self):

        self.__result = dict(STATUS="TRUE", VALUE=None)

    def set_status(self, p_res):

        if p_res:
            self.__result["STATUS"] = "TRUE"
        else:
            self.__result["STATUS"] = "FALSE"

    def set_db_result(self, p_values):

        self.__result["VALUE"] = []

        if p_values is not None:
            for t_data in p_values:
                self.__result["VALUE"].append(t_data.to_json())

    def set_str_result(self, p_value):

        if p_value is None:
            self.__result["VALUE"] = ""
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
    post interface
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
        _logger.error("Invoke %s failed, parameter is %s, status is %s" % (p_url, _para, _result["STATUS"]))
        return None

    return _result["VALUE"]


def orc_get_parameter():
    """
    Get parameter for post interface
    :return:
    """
    return request.json


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
