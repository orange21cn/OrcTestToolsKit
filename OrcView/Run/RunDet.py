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

        service = RunDetService()
        self.usr_set_service(service)
        self.usr_chk_able()


class RunDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewRunDet(QWidget):

    def __init__(self, p_def):

        QWidget.__init__(self)

        self.__table_def = p_def
        self.__resource_run = OrcHttpResource("Run")

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

        # Buttons window
        _btn_definition = [
            dict(id="run", name=u'执行')
        ]
        _wid_buttons = ViewButtons(_btn_definition)
        _wid_buttons.align_back()

        # 底部按钮及进度条
        _layout_bottom = QHBoxLayout()
        _layout_bottom.addWidget(self.__progress)
        _layout_bottom.addWidget(_wid_buttons)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addLayout(_layout_bottom)

        self.setLayout(_layout)

        _wid_buttons.sig_clicked.connect(self.__operate)

    def __operate(self, p_flg):

        if "run" == p_flg:
            self.__resource_run.put(self.__path)
        else:
            pass

    def usr_refresh(self, p_path):

        self.__path = dict(path=p_path)

        self.__model.usr_search(self.__path)

        self.__progress.setValue(90)
