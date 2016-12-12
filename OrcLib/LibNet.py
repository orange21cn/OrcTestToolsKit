# coding=utf-8
import json
import requests
import socket

from exceptions import ValueError
from functools import wraps
from flask import make_response
from flask import request
from requests.exceptions import RequestException
from requests.packages.urllib3.exceptions import HTTPError
from OrcLib.LibLog import OrcLog
from OrcLib import get_config
from OrcApi import orc_db

_logger = OrcLog("basic.lib_net")


class OrcResourceBase(object):
    """
    http 服务调用封装为资源
    """
    def __init__(self, p_mod):

        object.__init__(self)

        mod_list = dict(BatchDef='BATCH',
                        BatchDet='BATCH',
                        CaseDef='CASE',
                        CaseDet='CASE',
                        StepDef='CASE',
                        StepDet='CASE',
                        Item='CASE',
                        Data='DATA',
                        PageDef='WEB_LIB',
                        PageDet='WEB_LIB',
                        WindowDef='WEB_LIB',
                        WidgetDef='WEB_LIB',
                        WidgetDet='WEB_LIB',
                        Driver='DRIVER',
                        RunDef='RUN',
                        RunDet='RUN',
                        Run='RUN',
                        View="VIEW",
                        DriverWeb='SERVER_WEB_001',
                        Report="REPORT",
                        Dict='DEFAULT',
                        RunTime='DEFAULT')

        flag = None if p_mod not in mod_list else mod_list[p_mod]

        self._configer = get_config("network")
        self._ip = self._configer.get_option(flag, "ip")
        self._port = int(self._configer.get_option(flag, "port"))
        self._version = self._configer.get_option(flag, "version")
        self._url = "http://%s:%s/api/%s/%s" % (self._ip, self._port, self._version, p_mod)

    def get_url(self):
        return self._url


class OrcSocketResource(OrcResourceBase):

    def __init__(self, p_mod):

        OrcResourceBase.__init__(self, p_mod)

    def get(self, p_para):
        """
        :param p_para:
        :return:
        """
        import time

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self._ip, self._port))

        time.sleep(2)
        sock.send(json.dumps(p_para))
        _msg = sock.recv(1024)
        sock.close()

        return _msg


class OrcHttpNewResource(OrcResourceBase):
    """
    http 服务调用封装为资源
    """
    def __init__(self, p_mod):

        OrcResourceBase.__init__(self, p_mod)

        self.__back_url = self._url

    def set_path(self, p_id=None):

        if p_id is None:
            self._url = self.__back_url
        else:
            self._url = "%s/%s" % (self.__back_url, p_id)

    def __restore_url(self):
        if self.__back_url != self._url:
            self._url = self.__back_url

    def get(self, p_cond=None):
        """
        :param p_cond:
        :param p_cond: dict
        :return:
        """
        res = self.__invoke("GET", self._url, p_cond)
        self.__restore_url()

        return res

    def post(self, p_cond=None):
        """
        :param p_cond:
        """
        res = self.__invoke("POST", self._url, p_cond)
        self.__restore_url()

        return res

    def put(self, p_cond=None):
        """
        :param p_cond:
        :return:
        """
        res = self.__invoke("PUT", self._url, p_cond)
        self.__restore_url()

        return res

    def delete(self, p_cond=None):
        """
        :param p_cond:
        :return:
        """
        res = self.__invoke("DELETE", self._url, p_cond)
        self.__restore_url()

        return res

    @staticmethod
    def __invoke(p_flg, p_url, p_para):

        _type = {'content-type': 'application/json'}

        _para = OrcParameter.send_para(p_para)
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


class OrcParameter:
    """
    参数处理,防止非 dict 类型无法传输
    """

    def __init__(self):
        pass

    @staticmethod
    def send_para(p_para):
        """
        发送参数
        :param p_para:
        :return:
        """
        _parameter = dict(para=p_para)
        return json.dumps(_parameter)

    @staticmethod
    def receive_para():
        """
        接收参数
        :return:
        """
        _parameter = request.json
        return _parameter["para"]


class OrcResult(object):
    """
    处理返回值
    """
    def __init__(self, p_res=None):

        object.__init__(self)

        self.status = True
        self.data = None

        # 加载并处理返回值
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
        # 数据库对象
        if isinstance(p_data, orc_db.Model):
            self.data = p_data.to_json()

        # 数据库对象数组
        elif isinstance(p_data, list) \
                and 0 < len(p_data) \
                and isinstance(p_data[0], orc_db.Model):

            self.data = []
            for t_data in p_data:
                self.data.append(t_data.to_json())

        # 其他数据类型
        else:
            self.data = p_data

    def rtn(self):
        """
        返回信息字符串
        :return:
        """
        _result = dict(STATUS=self.status,
                       DATA=self.data)
        return _result


def orc_api(p_func):
    """
    接口预处理
    :param p_func:
    :return:
    """
    def api_func(*args, **kwargs):

        from OrcLib.LibException import OrcApiModelFailException

        # 返回值
        result = OrcResult()

        try:
            # 函数调用
            _rtn = p_func(*args, **kwargs)

            # 设置返回值
            result.set_status(True)
            result.set_data(_rtn)

        except OrcApiModelFailException:
            result.set_status(False)

        return result.rtn()

    return api_func
