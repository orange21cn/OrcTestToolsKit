# coding=utf-8
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcView.Data.Data.DataAdd import ViewDataAdd
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Lib.LibViewDef import def_view_case_def
from .CaseModel import CaseModel


class CaseControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'Case')


class CaseView(QWidget):

    sig_case_det = OrcSignal(dict)
    sig_selected = OrcSignal([dict])

    def __init__(self, p_type=None):

        QWidget.__init__(self)

        self.title = u"用例管理"

        self._type = p_type

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_case_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Data result display widget
        self.display = ViewTree('Case', CaseModel, CaseControl)

        # Context menu
        if self._type is None:

            self.display.create_context_menu([
                dict(NAME=u"增加", STR="sig_add"),
                dict(NAME=u"删除", STR="sig_del"),
                dict(NAME=u"增加数据", STR="sig_data"),
                dict(NAME=u"添加至运行", STR="sig_run")])

            # 右键菜单
            self.display.sig_context.connect(self.context)

        # Buttons widget
        if self._type is None:
            wid_buttons = OrcButtons([
                dict(id="add", name=u"增加"),
                dict(id="delete", name=u"删除"),
                dict(id="update", name=u"修改", type="CHECK"),
                dict(id="search", name=u"查询"),
                dict(id="test", name=u"取消")
            ])

            # 双击打开用例发双击信号
            self.display.doubleClicked[QModelIndex].connect(self.case_detail)

        elif 'SINGLE' == self._type:
            wid_buttons = OrcButtons([
                dict(id="search", name=u"查询"),
                dict(id="cancel", name=u"取消")
            ])

            self.display.model.checkable()

            # 双击选择用例
            self.display.doubleClicked.connect(self.select_one)

        elif 'MULTI' == self._type:
            wid_buttons = OrcButtons([
                dict(id="select", name=u"选择"),
                dict(id="search", name=u"查询"),
                dict(id="cancel", name=u"取消")
            ])

        else:
            wid_buttons = OrcButtons([])

        # win add case
        self.__win_add = ViewAdd(def_view_case_def)

        # win add data
        self.__win_data = ViewDataAdd()

        # Layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.__wid_search_cond)
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        self.setLayout(layout_main)

        # 点击按钮操作
        wid_buttons.sig_clicked.connect(self.operate)

        # 增加
        self.__win_add.sig_submit[dict].connect(self.add)

    def search(self):
        """
        查询
        :return:
        """
        self.display.model.mod_search(self.__wid_search_cond.get_cond())

    def add(self, p_data):
        """
        增加用例
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
            if OrcMessage.question(self, u'确认删除'):
                self.display.model.mod_delete()
        elif "update" == p_flag:
            self.display.model.editable()
        elif "search" == p_flag:
            self.search()
        if "select" == p_flag:
            self.select()
        elif "cancel" == p_flag:
            self.close()
        elif "test" == p_flag:
            self.test()
        else:
            pass

    def case_detail(self, p_index):
        """
        双击信号用于展开用例步骤界面
        :param p_index:
        :return:
        """
        if not self.display.model.mod_get_editable():

            _id = self.display.model.node(p_index).content["id"]
            _no = self.display.model.node(p_index).content["case_no"]
            _data = {"id": _id, "no": _no}

            self.sig_case_det[dict].emit(_data)

    def context(self, p_flag):
        """
        右键菜单
        :param p_flag:
        :return:
        """
        if "sig_data" == p_flag:

            _id = self.display.model.mod_get_current_data().content["id"]

            self.__win_data.show()
            self.__win_data.set_src_type("CASE")
            self.__win_data.set_src_id(_id)

        elif "sig_run" == p_flag:

            case_id = self.display.model.mod_get_current_data().content["id"]
            self.display.model.service_run(case_id)

    def select(self):
        """
        选择多个用例
        :return:
        """
        _res = self.display.model.mod_get_checked()
        self.sig_selected[dict].emit(_res)
        self.close()

    def select_one(self):
        """
        选择一个用例
        :return:
        """
        _res = self.display.model.mod_get_current_data().content["id"]
        self.sig_selected[dict].emit([_res])
        self.close()


# @orc_singleton
# class CaseView(CaseBaseView):
#
#     def __init__(self):
#
#         CaseBaseView.__init__(self)
#
#
# class CaseSelectView(CaseBaseView):
#
#     def __init__(self):
#
#         CaseBaseView.__init__(self, 'MULTI')
#
#
# class FuncSelectView(CaseBaseView):
#
#     def __init__(self):
#
#         CaseBaseView.__init__(self, 'SINGLE')
#
#         self.display.model.set_checkable(False)
