# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibViewDef import def_view_widget_det

from .WidgetDetModel import WidgetDetModel


class WidgetDetControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'WidgetDet')


class WidgetDetView(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        # Current widget id
        self.__widget_id = None

        # Data result display widget
        self.display = ViewTable('WidgetDet', WidgetDetModel, WidgetDetControl)

        # Buttons widget
        wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="up", name=u"上移"),
            dict(id="down", name=u"下移")
        ])

        # win_add
        self.__win_add = ViewAdd(def_view_widget_det)

        # Layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # 点击按钮
        wid_buttons.sig_clicked.connect(self.operate)

        # 新增
        self.__win_add.sig_submit[dict].connect(self.add)

    def add_show(self):
        """
        显示新增弹出框
        :return:
        """
        if self.__widget_id is not None:
            self.__win_add.show()

    def add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        _data = p_data
        _data["widget_id"] = self.__widget_id
        self.display.model.mod_add(_data)

    def set_widget_id(self, p_widget_id):
        """
        设置控件 id
        :param p_widget_id:
        :return:
        """
        self.__widget_id = p_widget_id
        self.display.model.mod_search({"widget_id": self.__widget_id})

    def clean(self):
        """
        清空
        :return:
        """
        self.__widget_id = None
        self.display.model.mod_clean()

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
        elif "update" == p_flag:
            self.display.model.mod_editable()
        elif "up" == p_flag:
            self.display.model.mod_up()
        elif "down" == p_flag:
            self.display.model.mod_down()
        else:
            pass
