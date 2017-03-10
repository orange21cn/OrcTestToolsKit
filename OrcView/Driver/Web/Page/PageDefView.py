# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibViewDef import def_view_page_def

from .PageDefModel import PageDefModel


class PageDefControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'PageDef')


class PageDefView(QWidget):

    sig_selected = OrcSignal(str)
    sig_search = OrcSignal()
    sig_delete = OrcSignal()

    def __init__(self, p_type=None):

        QWidget.__init__(self)

        self.title = u"用例管理"

        self.__type = p_type

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_page_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Data result display widget
        self.display = ViewTable('PageDef', PageDefModel, PageDefControl)

        # Buttons widget
        if p_type is None:
            wid_buttons = ViewButtons([
                dict(id="add", name=u"增加"),
                dict(id="delete", name=u"删除"),
                dict(id="update", name=u"修改", type="CHECK"),
                dict(id="search", name=u"查询")
            ])

            # 单击更新页面内容界面
            self.display.clicked[QModelIndex].connect(self.select)
        else:
            wid_buttons = ViewButtons([dict(id="search", name=u"查询")])
            self.display.doubleClicked.connect(self.select)

        # win_add
        self.__win_add = ViewAdd(def_view_page_def)

        # Layout
        layout_main = QVBoxLayout()
        if self.__type is not None:
            layout_main.addWidget(self.__wid_search_cond)
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # 点击按钮操作
        wid_buttons.sig_clicked.connect(self.operate)

        # 新增
        self.__win_add.sig_submit[dict].connect(self.add)

    def search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        self.display.model.mod_search(p_cond)

    def add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        self.display.model.mod_add(p_data)

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
            self.display.model.mod_editable()
        elif "search" == p_flag:
            if self.__type is None:
                self.sig_search.emit()
            else:
                self.display.model.mod_search(self.__wid_search_cond.get_cond())
        else:
            pass

    def select(self, p_index):
        """
        单击后释放信号用于更新页面内容界面
        :param p_index:
        :return:
        """
        _page_id = self.display.model.mod_get_data(p_index.row())["id"]
        self.sig_selected[str].emit(str(_page_id))

        # _node = self.__model.usr_get_data(p_index.row())
        # _id = _node["id"]
        # _flag = _node["page_flag"]
        #
        # self.sig_selected.emit(dict(id=str(_id), flag=_flag))

        if self.__type is not None:
            self.close()
