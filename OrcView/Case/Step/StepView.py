# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QWidget

from OrcView.Data.Data.DataAdd import ViewDataAdd
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibViewDef import def_view_step
from .StepModel import StepModel


class StepControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'Step')


class StepView(QWidget):

    sig_select = OrcSignal(str)
    sig_search = OrcSignal()
    sig_delete = OrcSignal()

    def __init__(self, p_id):

        QWidget.__init__(self)

        self.__case_id = p_id

        # Data result display widget
        self.display = ViewTable('Step', StepModel, StepControl)

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

        # win_add
        self.__win_add = ViewAdd(def_view_step)

        # win add data
        self.__win_data = ViewDataAdd()

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

        # 新增
        self.__win_add.sig_submit.connect(self.add)

        # 右键菜单
        self.display.sig_context.connect(self.context)

    def add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        self.display.model.mod_add(
            dict(case_det={"case_id": self.__case_id}, step=p_data))

    def operate(self, p_flag):
        """
        点击按钮操作
        :param p_flag:
        :return:
        """
        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.display.model.mod_delete()
            self.sig_delete.emit()
        elif "update" == p_flag:
            self.display.model.editable()
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

            self.__win_data.show()
            self.__win_data.set_src_type("STEP")
            self.__win_data.set_src_id(_step_id)
