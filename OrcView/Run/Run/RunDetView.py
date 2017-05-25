# coding=utf-8
import time
import threading

from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibView import OrcProcess
from OrcView.Lib.LibTree import ViewTree

from .RunDetModel import RunDetModel
from .RunDetModel import RunDetControl


class RunDetView(QWidget):

    sig_stop = OrcSignal()

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

        # 更新数据
        self.__progress.sig_finish.connect(self.sig_stop.emit)

    def usr_update(self):
        """
        更新数据
        :return:
        """
        while True:

            # 检查用户停止状态
            usr_status = self.display.model.service_get_usr_status()

            if not usr_status:
                self.__progress.reset()
                break

            # 实时数据读取列表,一次性读取,读取后会删除
            steps = self.display.model.service_get_steps()

            time.sleep(2)

            # 更新状态
            for _index in steps:

                self.display.model.mod_set_data(eval(steps[_index].replace('null,', 'None,')))
                self.__progress.step_forward()

            # 停止判断
            if 100 == self.__progress.get_process():
                self.sig_stop.emit()
                break

    def usr_refresh(self, p_path=None):
        """
        刷新
        :param p_path:
        :return:
        """
        if p_path is not None:
            self.__path = dict(path=p_path)

        # 更新用例列表
        self.display.model.mod_search(self.__path)

        # 更新进度条
        self.__progress.set_steps(self.display.model.service_item_nums())

    def usr_start(self):
        """
        开始执行,更新实时更新进度条,如果完成显示 100%,如果人为结束显示0%
        :return:
        """
        task = threading.Thread(target=self.usr_update)
        task.setDaemon(True)
        task.start()
