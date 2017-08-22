# coding=utf-8
import json
from PySide.QtGui import QWidget
from PySide.QtGui import QDialog
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibAdd import ViewNewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibViewDef import view_widget_def
from OrcView.Lib.LibMessage import OrcMessage

from .WidgetDefModel import WidgetDefModel


class WidgetDefControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'WidgetDef')


class WidgetDefView(QWidget):

    sig_selected = OrcSignal(dict)
    sig_search = OrcSignal()
    sig_delete = OrcSignal()

    def __init__(self, p_type=None):
        """
        支持选择类型,选择时按钮/查询条件/查询方式都有不同
        :param p_type:
        :return:
        """
        QWidget.__init__(self)

        self.__type = p_type

        # Search
        if self.__type is not None:
            self.__wid_search_cond = ViewSearch(view_widget_def, 2)

        # Data result display widget
        self.display = ViewTree(WidgetDefModel, WidgetDefControl)

        # Buttons window
        if self.__type is None:
            wid_buttons = OrcButtons([
                dict(id="add", name=u'增加'),
                dict(id="delete", name=u"删除"),
                dict(id="update", name=u"修改", type="CHECK"),
                dict(id="search", name=u"查询")
            ])

            # 界面单击操作
            self.display.clicked[QModelIndex].connect(self.widget_sig)

        elif 'SINGLE' == self.__type:
            wid_buttons = OrcButtons([
                dict(id="search", name=u"查询")
            ])

            # 禁止选择
            self.display.model.basic_checkable(False)

            # 双击选择
            self.display.doubleClicked[QModelIndex].connect(self.widget_sig)

        else:
            wid_buttons = OrcButtons([])

        # Layout
        layout_main = QVBoxLayout()

        if self.__type is not None:
            layout_main.addWidget(self.__wid_search_cond)

        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # 点击按钮
        wid_buttons.sig_clicked.connect(self.operate)

    def operate(self, p_flg):
        """
        点击按钮操作
        :param p_flg:
        :return:
        """
        if "add" == p_flg:
            _data = WidgetDefAdder.static_get_data()
            if _data is not None:
                self.display.model.mod_add(_data)

        elif "delete" == p_flg:
            if OrcMessage.question(self, u"确认删除"):
                self.display.model.mod_delete()
                self.sig_delete.emit()

        elif "update" == p_flg:
            self.display.model.basic_editable()

        elif "search" == p_flg:
            if self.__type is None:
                self.sig_search.emit()
            else:
                self.search(self.__wid_search_cond.get_cond())
        else:
            pass

    def search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return self.display.model.mod_search(p_cond)

    def widget_sig(self, p_index):
        """
        发送点击信号
        :param p_index:
        :return:
        """
        _widget_def = self.display.model.node(p_index).content
        self.sig_selected.emit(_widget_def)

        if self.__type is not None:
            self.close()


class WidgetDefAdder(ViewNewAdd):
    """
    新增计划控件
    """
    def __init__(self):

        ViewNewAdd.__init__(self, 'WidgetDef')

        self.setWindowTitle(u'新增控件')

    @staticmethod
    def static_get_data():

        view = WidgetDefAdder()
        view.exec_()

        return view._data


class WidgetDefSelector(QDialog):
    """

    """
    def __init__(self):

        QDialog.__init__(self)

        # Search
        self.__wid_search_cond = ViewSearch(view_widget_def, 2)

        # Data result display widget
        self.display = ViewTree(WidgetDefModel, WidgetDefControl)

        # Buttons window
        wid_buttons = OrcButtons([
            dict(id="search", name=u"查询")
        ])

        # 禁止选择
        self.display.model.basic_checkable(False)

        # Layout
        layout_main = QVBoxLayout()

        layout_main.addWidget(self.__wid_search_cond)
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        self.setLayout(layout_main)

        # 点击按钮
        wid_buttons.sig_clicked.connect(self.operate)

        # 双击后关闭
        self.display.doubleClicked.connect(self.close)

    def operate(self, p_flg):
        """
        点击按钮操作
        :param p_flg:
        :return:
        """
        if "search" == p_flg:
            self.display.model.mod_search(self.__wid_search_cond.get_cond())
        else:
            pass

    @staticmethod
    def get_widget():
        """

        :return:
        """
        view = WidgetDefSelector()
        view.exec_()

        return view.display.model.mod_get_current_data()
