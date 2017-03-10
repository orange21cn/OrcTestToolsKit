# coding=utf-8
import json
import socket


from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QThread
from PySide.QtCore import Signal as OrcSignal

from OrcLib import get_config
from OrcLib.LibLog import OrcLog
from OrcView.Lib.LibView import OrcProcess
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibControl import ControlBase

from .RunDetModel import RunDetModel


class RunDetControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'RunDet')


class RunDetView(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.__path = None
        self.__step_length = 0

        self.title = u"执行"

        # Data result display widget
        self.display = ViewTree('RunDet', RunDetModel, RunDetControl)

        # 进度条
        self.__progress = OrcProcess()

        # 底部按钮及进度条
        layout_bottom = QHBoxLayout()
        layout_bottom.addWidget(self.__progress)

        # Layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.display)
        layout_main.addLayout(layout_bottom)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # 进度条进程
        self.__thread_status = StatusReceiver()
        self.__thread_status.start()

        # 更新数据
        self.__thread_status.sig_status.connect(self.update_data)

    def update_data(self, p_data):
        """
        更新数据
        :param p_data:
        :return:
        """
        self.display.model.mod_set_data(p_data)
        self.__progress.step_forward()

    def usr_refresh(self, p_path=None):
        """
        刷新
        :param p_path:
        :return:
        """
        if p_path is not None:
            self.__path = dict(path=p_path)

        self.display.model.mod_search(self.__path)
        self.__progress.set_steps(self.display.model.service_item_nums())


class StatusReceiver(QThread):

    sig_status = OrcSignal(str)

    def __init__(self):

        QThread.__init__(self)

        self.__config = get_config("server")
        self.__logger = OrcLog("view")

    def run(self, *args, **kwargs):

        _ip = self.__config.get_option("VIEW", "ip")
        _port = int(self.__config.get_option("VIEW", "port"))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((_ip, _port))
        sock.listen(1)

        while True:

            connection, address = sock.accept()

            try:
                connection.settimeout(5)

                _cmd = connection.recv(1024)

                dict_cmd = json.loads(_cmd)
                if ("quit" in dict_cmd) and ("QUIT" == dict_cmd["quit"]):
                    break

                self.sig_status.emit(_cmd)

                connection.send(_cmd)

            except socket.timeout:
                self.__logger.error("time out")
            except Exception, err:
                self.__logger.error(err)

            connection.close()
