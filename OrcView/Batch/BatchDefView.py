# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcLib.LibProgram import orc_singleton
from OrcView.Data.Data.DataAdd import ViewDataAdd
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibViewDef import def_view_batch_def
from .BatchDefModel import BatchDefModel


class BatchDefControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'BatchDef')


@orc_singleton
class BatchDefView(QWidget):

    sig_batch_det = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"计划管理"

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_batch_def)
        self.__wid_search_cond.create()

        # Data result display widget
        self.display = ViewTree('BatchDef', BatchDefModel, BatchDefControl)

        # Context menu
        self.display.create_context_menu([
            dict(NAME=u"增加", STR="sig_add"),
            dict(NAME=u"删除", STR="sig_del"),
            dict(NAME=u"增加数据", STR="sig_data"),
            dict(NAME=u"添加至运行", STR="sig_run")])

        # Buttons widget
        wid_buttons = OrcButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="search", name=u"查询")
        ])

        # win_add
        self.__win_add = ViewAdd(def_view_batch_def)

        # win add data
        self.__win_data = ViewDataAdd()

        # Layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.__wid_search_cond)
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        self.setLayout(layout_main)

        # 按钮点击事件
        wid_buttons.sig_clicked.connect(self.operate)

        # 新增界面点击提交
        self.__win_add.sig_submit[dict].connect(self.display.model.mod_add)

        # 打开明细界面
        self.display.doubleClicked.connect(self.batch_detail)

        # 右键菜单
        self.display.sig_context.connect(self.context)

    def search(self):
        """
        查询
        :return:
        """
        self.display.model.mod_search(self.__wid_search_cond.get_cond())
        self.display.resizeColumnToContents(0)

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
        elif "search" == p_flag:
            self.search()
        else:
            pass

    def batch_detail(self, p_index):
        """
        显示计划详细信息
        :param p_index:
        :return:
        """
        if not self.display.model.mod_get_editable():

            _id = self.display.model.node(p_index).content["id"]
            _no = self.display.model.node(p_index).content["batch_no"]
            _data = dict(id=_id, no=_no)

            self.sig_batch_det[dict].emit(_data)

    def context(self, p_flag):
        """
        右键菜单
        :param p_flag:
        :return:
        """
        if "sig_data" == p_flag:

            _data = self.display.model.mod_get_current_data()
            _id = _data.content["id"]

            self.__win_data.show()
            self.__win_data.set_src_type("BATCH")
            self.__win_data.set_src_id(_id)

        elif "sig_run" == p_flag:

            batch_id = self.display.model.mod_get_current_data().content["id"]
            self.model.service_run(batch_id)
