# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import def_view_case_def

from CaseService import CaseDefService


class CaseSelModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self)

        self.usr_set_service(CaseDefService())


class CaseSelControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewCaseSelMag(QWidget):

    sig_selected = OrcSignal([dict])

    def __init__(self, p_type=None):

        QWidget.__init__(self)

        self.title = u"选择用例"

        self.__type = "MULTI" if p_type is None else p_type

        # Model
        self.__model = CaseSelModel()
        self.__model.usr_set_definition(def_view_case_def)

        if "SINGLE" == self.__type:
            self.__model.usr_chk_able()

        # Control
        _control = CaseSelControl(def_view_case_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_case_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        if "SINGLE" == self.__type:
            button_def = []
        else:
            button_def = [dict(id="select", name=u"选择")]

        button_def.extend([
            dict(id="search", name=u"查询"),
            dict(id="cancel", name=u"取消")])
        _wid_buttons = ViewButtons(button_def)

        # win_add
        self.__win_add = ViewAdd(def_view_case_def)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)
        _wid_display.clicked.connect(self.__model.usr_set_current_data)
        _wid_display.doubleClicked.connect(self.__select_one)

    def __operate(self, p_flag):

        if "select" == p_flag:
            self.__select()
        elif "search" == p_flag:
            self.__search()
        elif "cancel" == p_flag:
            self.close()
        else:
            pass

    def __search(self):
        self.__model.usr_search(self.__wid_search_cond.get_cond())

    def __select(self):
        _res = self.__model.usr_get_checked()
        self.sig_selected[dict].emit(_res)
        self.close()

    def __select_one(self):
        _res = self.__model.usr_get_current_data().content["id"]
        self.sig_selected[dict].emit([_res])
        self.close()
