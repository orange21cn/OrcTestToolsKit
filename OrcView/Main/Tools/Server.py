# coding=utf-8
import subprocess
from abc import abstractmethod

from PySide.QtGui import QPushButton

from OrcLib import get_config
from OrcLib.LibNet import OrcSocketResource
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibMain import LogClient


class ServerBase(QPushButton):

    def __init__(self, p_flag, p_name):

        QPushButton.__init__(self, p_name)

        self.setCheckable(True)

        # 日志
        self._logger = LogClient()

        # 通用配置
        self._configer = get_config()

        # 客户端配置
        self._configer_client = get_config("client")

        # HOME 目录
        self._home = self._configer.get_option("DEFAULT", "root")

        # 设置默认点击状态
        self._mode = self._configer_client.get_option(p_flag, 'mode')
        if "LOCAL" == self._mode:
            self.setChecked(True)

        # 服务
        self._service = None

        # 点击时执行
        self.pressed.connect(self.manage_service)

        # 设置样式
        self.setStyleSheet(get_theme("Buttons"))

    def __del__(self):

        if self._service is not None:
            self._service.kill()

    def _set_client_local(self, p_server, p_flag=None):
        """
        设置使用本地服务
        :param p_flag: 设置方式,ALL/IP/TYPE
        :param p_server:
        :return:
        """
        flag = "ALL" if p_flag is None else p_flag

        # 设置全用本地 IP
        if flag in ('ALL', 'IP'):
            local_ip = self._configer_client.get_option("DEFAULT", "local")
            self._configer_client.set_option(p_server, "ip", local_ip)

        # 设置使用本地方式调用(直接查询数据库,不通过接口调用)
        if flag in ('ALL', 'TYPE'):
            self._configer_client.set_option(p_server, "type", "LOCAL")

        # 设置使用本地服务器
        if flag in ('ALL', 'MODE'):
            self._configer_client.set_option(p_server, "mode", "LOCAL")

    def _set_client_remote(self, p_server, p_flag=None):
        """
        设置使用远程服务
        :param p_server:
        :param p_flag: 设置方式,ALL/IP/TYPE
        :return:
        """
        flag = "ALL" if p_flag is None else p_flag

        # 设置使用远程 IP
        if flag in ('ALL', 'IP'):
            remote_ip = self._configer_client.get_option("DEFAULT", "remote")
            self._configer_client.set_option(p_server, "ip", remote_ip)

        # 设置使用远程方式调用
        if flag in ('ALL', 'TYPE'):
            self._configer_client.set_option(p_server, "type", "REMOTE")

        # 设置服务端
        if flag in ('ALL', 'MODE'):
            self._configer_client.set_option(p_server, "mode", "REMOTE")

    @abstractmethod
    def manage_service(self):
        """
        服务及配置管理
        :return:
        """
        pass


class ServerResource(ServerBase):

    def __init__(self):

        ServerBase.__init__(self, 'BATCH', u'通用数据')

    def manage_service(self):

        servers = ('BATCH', 'CASE', 'DATA', 'WEB_LIB')

        # 客户端设置为远程
        if self.isChecked():

            for _server in servers:
                self._set_client_remote(_server)

            self._logger.put_message(u"设置通用数据远程调用")

        # 客户端设置为本地
        else:

            for _server in servers:
                self._set_client_local(_server)

            self._logger.put_message(u"设置通用数据本地调用")


class ServerRun(ServerBase):

    def __init__(self):

        ServerBase.__init__(self, 'RUN', u'运行')

    def manage_service(self):
        """
        管理 run 起停
        :return:
        """
        # 客户端设置为远程
        if self.isChecked():
            self._set_client_remote('RUN')
            self._logger.put_message(u"设置运行远程调用")

        # 客户端设置为本地
        else:
            self._set_client_local('RUN')
            self._logger.put_message(u"设置运行本地调用")


class ServerReport(ServerBase):

    def __init__(self):

        ServerBase.__init__(self, 'REPORT', u'报告')

        if 'LOCAL' == self._mode:
            self.start_service()

    def manage_service(self):
        """
        管理 report 起停
        :return:
        """
        # 客户端设置为远程
        if self.isChecked():

            # 关闭本地服务
            if self._service is not None:
                self._service.kill()

            # 客户端设置
            self._set_client_remote('REPORT')
            self._logger.put_message(u"关闭报告服务器")

        # 客户端设置为本地
        else:
            # 起动服务
            self.start_service()

            # 客户端设置
            self._set_client_local('REPORT', 'IP')
            self._set_client_local('REPORT', 'MODE')

            self._logger.put_message(u"起动报告服务器")

    def start_service(self):
        self._service = subprocess.Popen(["python", "%s/OrcApi/start_report.py" % self._home])


class ServerDriver(ServerBase):

    def __init__(self):

        ServerBase.__init__(self, 'DRIVER', u'驱动')

    def manage_service(self):
        """
        管理 api 起停
        :return:
        """
        # 客户端设置为远程
        if self.isChecked():
            self._set_client_remote('DRIVER')
            self._logger.put_message(u"关闭执行服务器")

        # 客户端设置为本地
        else:
            self._set_client_local('DRIVER')
            self._logger.put_message(u"起动执行服务器")


class ServerDebug(ServerBase):

    def __init__(self):

        ServerBase.__init__(self, 'SERVER_WEB_001', u'调试')

        if 'LOCAL' == self._mode:
            self.start_service()

    def __del__(self):

        if self._service is not None:
            self.stop_service()

    def manage_service(self):
        """
        管理 socket 起停
        :return:
        """
        # 当前为本地
        if self.isChecked():

            # 关闭本地服务
            if self._service is not None:
                self.stop_service()

            # 客户端设置为远程
            self._set_client_remote('SERVER_WEB_001')

            self._logger.put_message(u"关闭调试服务器")

        # 当前为远程
        else:
            # 起动服务
            self.start_service()

            # 客户端设置为本地
            self._set_client_local('SERVER_WEB_001', 'IP')
            self._set_client_local('SERVER_WEB_001', 'MODE')

            self._logger.put_message(u"起动调试服务器")

    def start_service(self):
        """
        起动服务
        :return:
        """
        self._service = subprocess.Popen(["python", "%s/OrcDriver/start_socket.py" % self._home])

    def stop_service(self):
        """
        关闭 socket 服务
        :return:
        """
        resource_debug = OrcSocketResource("DriverWeb")
        resource_debug.get(dict(quit="QUIT"))

        # 关闭进程
        self._service.kill()
