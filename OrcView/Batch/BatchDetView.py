# coding=utf-8
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcView.Case.Case.CaseView import CaseView
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibView import OrcPagination
from OrcView.Lib.LibViewDef import def_view_batch_det
from .BatchDetModel import BatchDetModel


class BatchDetControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'BatchDet')


class BatchDetView(QWidget):

    def __init__(self, p_data):

        QWidget.__init__(self)

        _batch_no = p_data["no"]
        self.__batch_id = p_data["id"]
        self.title = _batch_no

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_batch_det)
        self.__wid_search_cond.create()

        # Data result display widget
        self.display = ViewTable('BatchDet', BatchDetModel, BatchDetControl)

        # pagination
        self.__wid_pagination = OrcPagination()

        # Buttons widget
        wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="search", name=u"查询")
        ])

        # win_add
        self.__win_add = CaseView('MULTI')

        # button layout
        layout_bottom = QHBoxLayout()
        layout_bottom.addWidget(wid_buttons)
        layout_bottom.addStretch()
        layout_bottom.addWidget(self.__wid_pagination)

        # main layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.__wid_search_cond)
        layout_main.addWidget(self.display)
        layout_main.addLayout(layout_bottom)

        self.setLayout(layout_main)

        # 点击按钮事件
        wid_buttons.sig_clicked.connect(self.operate)

        # 分页
        self.__wid_pagination.sig_page.connect(self.search)

        # 新增
        self.__win_add.sig_selected.connect(self.add)

    def search(self):
        """
        查询
        :return:
        """
        _cond = self.__wid_search_cond.get_cond()
        _cond["batch_id"] = self.__batch_id
        self.display.model.mod_search(_cond)

    def add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        _data = {"batch_id": self.__batch_id, "case": p_data}
        self.display.model.mod_add(_data)

    def operate(self, p_flag):
        """
        点击按钮时操作
        :param p_flag:
        :return:
        """
        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.display.model.mod_delete()
        elif "search" == p_flag:
            self.search()
        else:
            pass
