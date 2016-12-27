# coding=utf-8
import json
import requests
import socket

from exceptions import ValueError
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

        # module configuration
        self._mod_config = dict(
            BatchDef=dict(config='BATCH', path="OrcApi.Batch.BatchApi"),
            BatchDet=dict(config='BATCH', path="OrcApi.Batch.BatchApi"),
            CaseDef=dict(config='CASE', path="OrcApi.Case.CaseApi"),
            CaseDet=dict(config='CASE', path="OrcApi.Case.CaseApi"),
            StepDef=dict(config='CASE', path="OrcApi.Case.CaseApi"),
            StepDet=dict(config='CASE', path="OrcApi.Case.CaseApi"),
            Item=dict(config='CASE', path="OrcApi.Case.CaseApi"),
            Data=dict(config='DATA', path="OrcApi.Case.DataApi"),
            PageDef=dict(config='WEB_LIB', path="OrcApi.Driver.Web.PageApi"),
            PageDet=dict(config='WEB_LIB', path="OrcApi.Driver.Web.PageApi"),
            WindowDef=dict(config='WEB_LIB', path="OrcApi.Driver.Web.WindowApi"),
            WidgetDef=dict(config='WEB_LIB', path="OrcApi.Driver.Web.WidgetApi"),
            WidgetDet=dict(config='WEB_LIB', path="OrcApi.Driver.Web.WidgetApi"),
            RunDef=dict(config='RUN', path="OrcApi.Run.RunApi"),
            RunDet=dict(config='RUN', path="OrcApi.Run.RunApi"),
            Run=dict(config='RUN', path="OrcApi.Run.RunApi"),
            Report=dict(config="REPORT", path="OrcApi.Run.ReportApi"),
            Dict=dict(config='DEFAULT', path="OrcApi.Lib.DictApi"),
            RunTime=dict(config='DEFAULT', path="OrcApi.RunTime.RunTimeApi"),
            Driver=dict(config='DRIVER', path="OrcDriver.DriverApi"),
            View=dict(config="VIEW", path=""),
            DriverWeb=dict(config='SERVER_WEB_001', path=""),
        )

        # Configuration
        self._configer = get_config("client")

        # module
        self._module = p_mod

        # flag for configuration
        self._flag = None if self._module not in self._mod_config else self._mod_config[self._module]["config"]

        # PATH
        self._path = None if self._module not in self._mod_config else self._mod_config[self._module]["path"]

        # IP
        self._ip = self._configer.get_option(self._flag, "ip")

        # PORT
        try:
            self._port = int(self._configer.get_option(self._flag, "port"))
        except TypeError:
            self._port = None

        # VERSION
        self._version = self._configer.get_option(self._flag, "version")

        # URL for remote api
        self._url = "http://%s:%s/api/%s/%s" % (self._ip, self._port, self._version, p_mod)

    # def get_url(self):
    #     return self._url


class OrcHttpService(OrcResourceBase):
    """
    Todo
    """
    def __init__(self, p_mod):

        OrcResourceBase.__init__(self, p_mod)

    def get(self, p_para):
        _para = OrcParameter.send_para(p_para)
        return requests.delete(self._url, data=_para)

    def post(self, p_para):
        _para = OrcParameter.send_para(p_para)
        return requests.delete(self._url, data=_para)

    def delete(self, p_para):
        _para = OrcParameter.send_para(p_para)
        return requests.delete(self._url, data=_para)

    def put(self, p_para):
        _para = OrcParameter.send_para(p_para)
        return requests.delete(self._url, data=_para)

    def save_pic(self, p_file_name):

        req = requests.get(self._url, stream=True)

        with open(p_file_name, 'wb') as _file:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    _file.write(chunk)
                    _file.flush()
            _file.close()


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


class OrcResource(OrcResourceBase):
    """
    资源调用,json/普通http
    """
    def __init__(self, module, mode=None):

        OrcResourceBase.__init__(self, module)

        self.__mode = "JSON" if mode is None else mode

        if "HTML" == self.__mode:
            self._header = {'content-type': "text/html"}
        elif "JSON" == self.__mode:
            self._header = {'content-type': "application/json"}
        else:
            self._header = self.__mode

    def post(self, path=None, parameter=None):
        """
        POST
        :param path:
        :param parameter:
        :return:
        """
        return self.action("POST", path, parameter)

    def delete(self, path=None, parameter=None):
        """
        DELETE
        :param path:
        :param parameter:
        :return:
        """
        return self.action("DELETE", path, parameter)

    def put(self, path=None, parameter=None):
        """
        PUT
        :param path:
        :param parameter:
        :return:
        """
        return self.action("PUT", path, parameter)

    def get(self, path=None, parameter=None):
        """
        GET
        :param path:
        :param parameter:
        :return:
        """
        return self.action("GET", path, parameter)

    def action(self, p_method, p_path, p_parameter):
        """
        调用,根据 method 来判断执行哪个函数
        :param p_method:
        :param p_path:
        :param p_parameter:
        :return:
        """
        result = None
        url_path = p_path if not isinstance(p_path, tuple) else "/".join(p_path)
        api_type = self._configer.get_option(self._flag, "type")

        # local api
        if "LOCAL" == api_type:
            try:
                # 导入模块
                _module = self.__get_module(p_path)

                # 获取函数
                _func = getattr(_module, "api_%s" % p_method.lower(), None)

                # 参数判断
                if p_path is None:
                    if p_parameter is None:
                        result = _func()
                    else:
                        result = _func(p_parameter)
                else:
                    if p_parameter is None:
                        result = _func(url_path)
                    else:
                        result = _func(url_path, p_parameter)

                # JSON 接口包装返回值
                if "JSON" == self.__mode:
                    result = self.__get_result(result)

            except (ImportError, AttributeError), err:
                print err
                _logger.error("function invoke error: %s" % err)

            return result

        # remote api
        else:
            try:
                _func = getattr(requests, p_method.lower())
                result = _func(url=self.__get_url(p_path),
                               data=OrcParameter.send_para(p_parameter),
                               headers=self._header)

                result = self.__get_http_result(result)
            except (HTTPError, ValueError, RequestException, AttributeError), err:
                _logger.error("function invoke error: %s" % err)

            return result

    def save_pic(self, p_path, p_file_name):
        """
        保存图片
        :param p_path:
        :param p_file_name:
        :return:
        """
        url_path = p_path if not isinstance(p_path, tuple) else "/".join(p_path)
        req = requests.get("%s/%s" % (self._url, url_path), stream=True)

        with open(p_file_name, 'wb') as _file:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    _file.write(chunk)
                    _file.flush()
            _file.close()

    def __get_module(self, p_path):
        """
        Dynamic import module
        :return:
        """
        if p_path is None:
            _name = "%sListAPI" % self._module
        else:
            _name = "%sAPI" % self._module

        return getattr(__import__(self._path, fromlist=True), _name)()

    def __get_url(self, p_path=None):
        """
        生成调用的 url
        :param p_path:
        :return:
        """
        if p_path is None:
            return self._url
        elif not isinstance(p_path, tuple):
            _logger.error("wrong path type, path: %s" % p_path)
            return
        else:
            return "%s/%s" % (self._url, "/".join(p_path))

    def __get_http_result(self, p_result):
        """
        对输出数据进行脱壳处理
        :param p_result:
        :return:
        """
        if not p_result.ok:

            result = OrcResult()
            result.set_data(p_result.ok)
            result.set_message(p_result.text)

            _logger.error("Invoke %s failed, response is %s" % (self._url, p_result.ok))

            return result

        else:
            return self.__get_result(p_result.text)

    def __get_result(self, p_result):
        """
        对输出数据进行脱壳处理
        :param p_result:
        :return:
        """
        if "JSON" == self.__mode:
            return OrcResult(p_result)
        else:
            return p_result


class OrcHttpResource(OrcResourceBase):
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
            _logger.error("Invoke %s failed, parameter is %s, status is" % (p_url, _para))
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
        if not _parameter:
            return dict()
        else:
            return _parameter["para"]


class OrcResult(object):
    """
    处理返回值
    """
    def __init__(self, p_res=None):

        object.__init__(self)

        self.status = False
        self.message = None
        self.data = None

        # 加载并处理返回值
        if p_res is not None:

            _res = p_res

            if not isinstance(p_res, dict):
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

    def set_message(self, p_message):
        """
        设置返回信息
        :param p_message:
        :return:
        """
        self.message = p_message

    def rtn(self):
        """
        返回信息字符串
        :return:
        """
        _result = dict(STATUS=self.status,
                       MESSAGE=self.message,
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
