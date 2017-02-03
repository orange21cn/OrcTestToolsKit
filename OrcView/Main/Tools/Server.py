# coding=utf-8
import subprocess
from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QPushButton
from OrcLib import get_config
from OrcLib.LibNet import OrcSocketResource
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibMain import LogClient


class Server(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        # 起动 api
        self.btn_api = QPushButton(u"通用数据")
        self.btn_api.setCheckable(True)

        # 起动 run
        self.btn_run = QPushButton(u"运行")
        self.btn_run.setCheckable(True)

        # 起动 report
        self.btn_report = QPushButton(u"报告")
        self.btn_report.setCheckable(True)

        # 起动 driver
        self.btn_driver = QPushButton(u"驱动")
        self.btn_driver.setCheckable(True)

        # 起动 socket
        self.btn_socket = QPushButton(u"调试")
        self.btn_socket.setCheckable(True)

        # layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.btn_api)
        main_layout.addWidget(self.btn_run)
        main_layout.addWidget(self.btn_report)
        main_layout.addWidget(self.btn_driver)
        main_layout.addWidget(self.btn_socket)

        self.setLayout(main_layout)

        # connection
        self.btn_api.pressed.connect(self.mag_api)
        self.btn_report.pressed.connect(self.mag_report)
        self.btn_run.pressed.connect(self.mag_run)
        self.btn_driver.pressed.connect(self.mag_driver)
        self.btn_socket.pressed.connect(self.mag_socket)

        # 设置样式
        self.setStyleSheet(get_theme("Buttons"))

        # variable
        self.configer = get_config()
        self.configer_client = get_config("client")
        self.logger = LogClient()
        self.home = self.configer.get_option("DEFAULT", "root")

        self.service_api = None
        self.service_run = None
        self.service_report = None
        self.service_driver = None
        self.service_socket = None

    def __del__(self):

        try:
            # 关闭 api
            if self.service_api is not None:
                self.service_api.kill()

            # 关闭 run
            if self.service_run is not None:
                self.service_run.kill()

            # 关闭 report
            if self.service_report is not None:
                self.service_report.kill()

            # 关闭 driver
            if self.service_driver is not None:
                self.service_driver.kill()

            # 关闭 socket
            if self.service_socket is not None:
                # 关闭 socket 服务
                resource_debug = OrcSocketResource("DriverWeb")
                resource_debug.get(dict(quit="QUIT"))

                # 关闭进程
                self.service_socket.kill()

        except Exception, err:
            self.logger.put_error(u"关闭服务失败: %s" % err)

    def mag_api(self):
        """
        管理 api 起停
        :return:
        """
        servers = ('BATCH', 'CASE', 'DATA', 'WEB_LIB')

        # 当前为本地
        if self.btn_api.isChecked():

            # 客户端设置为远程
            for _server in servers:
                self.set_client_remote(_server)

            self.logger.put_message(u"关闭通用数据服务器")

        # 当前为远程
        else:
            # 客户端设置为本地
            for _server in servers:
                self.set_client_local(_server)

            self.logger.put_message(u"起动通用数据服务器")

    def mag_report(self):
        """
        管理 report 起停
        :return:
        """
        # 当前为本地
        if self.btn_report.isChecked():

            # 关闭本地服务
            if self.service_report is not None:
                self.service_report.kill()

            # 客户端设置为远程
            self.set_client_remote('REPORT')

            self.logger.put_message(u"关闭报告服务器")

        # 当前为远程
        else:
            # 起动服务
            self.service_report = subprocess.Popen(["python", "%s/OrcApi/start_report.py" % self.home])

            # 客户端设置为本地
            self.set_client_local('REPORT')

            self.logger.put_message(u"起动报告服务器")

    def mag_run(self):
        """
        管理 api 起停
        :return:
        """
        # 当前为本地
        if self.btn_run.isChecked():

            # 客户端设置为远程
            self.set_client_remote('RUN')

            self.logger.put_message(u"关闭执行服务器")

        # 当前为远程
        else:

            # 客户端设置为本地
            self.set_client_local('RUN')

            self.logger.put_message(u"起动执行服务器")

    def mag_driver(self):
        """
        管理 driver 起停
        :return:
        """
        # 当前为本地
        if self.btn_driver.isChecked():

            # 关闭本地服务
            if self.service_driver is not None:
                self.service_driver.kill()

            # 客户端设置为远程
            self.set_client_remote('DRIVER')

            self.logger.put_message(u"关闭驱动服务器")

        # 当前为远程
        else:

            # 起动服务
            self.service_driver = subprocess.Popen(["python", "%s/OrcDriver/start_driver.py" % self.home])

            # 客户端设置为本地
            self.set_client_local('DRIVER', 'IP')

            self.logger.put_message(u"起动驱动服务器")

    def mag_socket(self):
        """
        管理 socket 起停
        :return:
        """
        # 当前为本地
        if self.btn_socket.isChecked():

            # 关闭本地服务
            if self.service_socket is not None:
                # 关闭 socket 服务
                resource_debug = OrcSocketResource("DriverWeb")
                resource_debug.get(dict(quit="QUIT"))

                # 关闭进程
                self.service_socket.kill()

            # 客户端设置为远程
            self.set_client_remote('SERVER_WEB_001')

            self.logger.put_message(u"关闭调试服务器")

        # 当前为远程
        else:
            # 起动服务
            self.service_socket = subprocess.Popen(["python", "%s/OrcDriver/start_socket.py" % self.home])

            # 客户端设置为本地
            self.set_client_local('SERVER_WEB_001', 'IP')

            self.logger.put_message(u"起动调试服务器")

    def set_client_local(self, p_server, p_flag=None):
        """
        设置使用本地服务
        :param p_flag: 设置方式,ALL/IP/TYPE
        :param p_server:
        :return:
        """
        flag = "ALL" if p_flag is None else p_flag

        if flag in ('ALL', 'IP'):
            local_ip = self.configer_client.get_option("DEFAULT", "local")
            self.configer_client.set_option(p_server, "ip", local_ip)

        if flag in ('ALL', 'TYPE'):
            self.configer_client.set_option(p_server, "type", "LOCAL")

    def set_client_remote(self, p_server, p_flag=None):
        """
        设置使用远程服务
        :param p_server:
        :param p_flag: 设置方式,ALL/IP/TYPE
        :return:
        """
        flag = "ALL" if p_flag is None else p_flag

        if flag in ('ALL', 'IP'):
            remote_ip = self.configer_client.get_option("DEFAULT", "remote")
            self.configer_client.set_option(p_server, "ip", remote_ip)

        if flag in ('ALL', 'TYPE'):
            self.configer_client.set_option(p_server, "type", "REMOTE")
