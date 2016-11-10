# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QProgressBar

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibTree import ModelNewTree
from OrcView.Lib.LibControl import LibControl
from OrcLib.LibNet import OrcHttpResource
from RunDetService import RunDetService


class RunDetModel(ModelNewTree):

    def __init__(self):

        ModelNewTree.__init__(self)

        self.__service = RunDetService()
        self.usr_set_service(self.__service)
        self.usr_chk_able()

    def model_run(self, p_path):
        self.__service.usr_run(p_path)


class RunDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewRunDet(QWidget):

    def __init__(self, p_def):

        QWidget.__init__(self)

        self.__table_def = p_def
        self.__path = None

        self.title = u"执行"

        # Model
        self.__model = RunDetModel()
        self.__model.usr_set_definition(self.__table_def)

        # Control
        _control = RunDetControl(self.__table_def)

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # 进度条
        self.__progress = QProgressBar()

        # 底部按钮及进度条
        _layout_bottom = QHBoxLayout()
        _layout_bottom.addWidget(self.__progress)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addLayout(_layout_bottom)

        self.setLayout(_layout)

    def usr_refresh(self, p_path):

        self.__path = dict(path=p_path)

        self.__model.usr_search(self.__path)

        self.__progress.setValue(90)
