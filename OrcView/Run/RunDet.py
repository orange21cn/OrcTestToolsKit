# coding=utf-8
import socket
import json

from PySide.QtCore import QThread
from PySide.QtCore import Signal as OrcSignal

from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QHBoxLayout

from OrcLib import get_config
from OrcLib.LibLog import OrcLog

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibTree import ModelNewTree
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibView import OrcProcess
from OrcView.Lib.LibViewDef import def_view_run_det
from RunDetService import RunDetService


class RunDetModel(ModelNewTree):

    def __init__(self):

        ModelNewTree.__init__(self)

        self.__service = RunDetService()
        self.usr_set_service(self.__service)
        self.usr_chk_able()

    def model_run(self, p_path):
        self.__service.usr_run(p_path)

    def get_item_nums(self, p_node=None):

        count = 0

        if p_node is None:
            node = self._state_root
        else:
            node = p_node

        if node.content is not None:
                count = 1

        if node.children:
            for child in node.children:
                count += self.get_item_nums(child)

        return count


class RunDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewRunDet(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.__path = None
        self.__step_length = 0

        self.title = u"执行"

        # Model
        self.__model = RunDetModel()
        self.__model.usr_set_definition(def_view_run_det)

        # Control
        _control = RunDetControl(def_view_run_det)

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # 进度条
        self.__progress = OrcProcess()

        # 底部按钮及进度条
        _layout_bottom = QHBoxLayout()
        _layout_bottom.addWidget(self.__progress)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addLayout(_layout_bottom)

        self.setLayout(_layout)

        self.__thread_status = StatusReceiver()
        self.__thread_status.start()

        self.__thread_status.sig_status.connect(self.update_data)

    def update_data(self, p_data):
        self.__model.usr_set_data(p_data)
        self.__progress.step_forward()

    def usr_refresh(self, p_path=None):

        if p_path is not None:
            self.__path = dict(path=p_path)

        self.__model.usr_search(self.__path)
        self.__progress.set_steps(self.__model.get_item_nums())


class StatusReceiver(QThread):

    sig_status = OrcSignal(str)

    def __init__(self):

        QThread.__init__(self)

        self.__config = get_config("network")
        self.__logger = OrcLog("view")

    def run(self, *args, **kwargs):

        _ip = self.__config.get_option("VIEW", "ip")
        _port = int(self.__config.get_option("VIEW", "port"))

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((_ip, _port))
        sock.listen(1)

        while True:

            connection, address = sock.accept()

            try:
                connection.settimeout(5)

                _cmd = connection.recv(1024)
                self.sig_status.emit(_cmd)

                connection.send(_cmd)

            except socket.timeout:
                self.__logger.error("time out")
            except Exception, err:
                self.__logger.error(err)

            connection.close()
