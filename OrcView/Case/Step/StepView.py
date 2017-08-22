# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QWidget

from OrcView.Data.Data.DataAdd import DataAdder
from OrcView.Lib.LibAdd import ViewNewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibMessage import OrcMessage

from .StepModel import StepModel


class StepControl(ControlBase):

    def __init__(self, p_def='Step'):

        ControlBase.__init__(self, p_def)


class StepView(QWidget):

    sig_select = OrcSignal(str)
    sig_search = OrcSignal()
    sig_delete = OrcSignal()

    def __init__(self, p_id):

        QWidget.__init__(self)

        self.__case_id = p_id

        # Data result display widget
        self.display = ViewTable(StepModel, StepControl)

        # Context menu
        menu_def = [dict(NAME=u"增加", STR="sig_add"),
                    dict(NAME=u"删除", STR="sig_del"),
                    dict(NAME=u"增加数据", STR="sig_data")]

        self.display.create_context_menu(menu_def)

        # Buttons widget
        wid_buttons = OrcButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="up", name=u"上移"),
            dict(id="down", name=u"下移")
        ], "VER")

        # Layout
        layout_main = QHBoxLayout()
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # 生成界面初始数据
        self.display.model.mod_search(dict(case_id=p_id))

        # 按钮点击操作
        wid_buttons.sig_clicked.connect(self.operate)

        # 单击发出单击事件
        self.display.clicked.connect(self.selected)

        # 右键菜单
        self.display.sig_context.connect(self.context)

    def operate(self, p_flag):
        """
        点击按钮操作
        :param p_flag:
        :return:
        """
        if "add" == p_flag:
            _data = StepAdder.static_get_data()
            if _data is not None:
                self.display.model.mod_add(dict(case_det=dict(case_id=self.__case_id), step=_data))
        elif "delete" == p_flag:
            if OrcMessage.question(self, u'确认删除'):
                self.display.model.mod_delete()
                self.sig_delete.emit()
        elif "update" == p_flag:
            self.display.model.basic_editable()
        elif "up" == p_flag:
            self.display.model.mod_up()
        elif "down" == p_flag:
            self.display.model.mod_down()
        else:
            pass

    def selected(self, p_index):
        """
        发出单击事件用于显示步骤执行项
        :param p_index:
        :return:
        """
        _index = p_index.row()
        _step_id = self.display.model.mod_get_data(_index)["step_id"]

        self.sig_select.emit(_step_id)

    def context(self, p_flag):
        """
        右键菜单
        :param p_flag:
        :return:
        """
        if "sig_data" == p_flag:
            _step_id = self.display.model.mod_get_current_data()["step_id"]
            DataAdder.static_add_data("STEP", _step_id)


class StepAdder(ViewNewAdd):
    """
    新增计划控件
    """
    def __init__(self):

        ViewNewAdd.__init__(self, 'Step')

        self.setWindowTitle(u'新增步骤')

    @staticmethod
    def static_get_data():

        view = StepAdder()
        view.exec_()

        return view._data
