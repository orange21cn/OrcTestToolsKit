# coding=utf-8
import json
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibViewDef import def_view_widget_def

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
            self.__wid_search_cond = ViewSearch(def_view_widget_def)
            self.__wid_search_cond.set_col_num(2)
            self.__wid_search_cond.create()

        # Data result display widget
        self.display = ViewTree('WidgetDef', WidgetDefModel, WidgetDefControl)

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
            self.display.model.checkable(False)

            # 双击选择
            self.display.doubleClicked[QModelIndex].connect(self.widget_sig)

        else:
            wid_buttons = OrcButtons([])

        # win_add
        self.__win_add = ViewAdd(def_view_widget_def)

        # Layout
        layout_main = QVBoxLayout()

        if self.__type is not None:
            layout_main.addWidget(self.__wid_search_cond)

        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # 新增
        self.__win_add.sig_submit[dict].connect(self.display.model.mod_add)

        # 点击按钮
        wid_buttons.sig_clicked.connect(self.operate)

    def operate(self, p_flg):
        """
        点击按钮操作
        :param p_flg:
        :return:
        """
        if "add" == p_flg:
            self.__win_add.show()

        elif "delete" == p_flg:
            self.display.model.mod_delete()
            self.sig_delete.emit()

        elif "update" == p_flg:
            self.display.model.editable()

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
