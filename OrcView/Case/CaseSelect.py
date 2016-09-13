# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibControl import LibControl


class CaseSelModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self)

        i_base_url = 'http://localhost:5000/CaseDef'
        _interface = {
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class CaseSelControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewCaseSelMag(QWidget):

    sig_selected = OrcSignal([dict])

    def __init__(self):

        QWidget.__init__(self)

        _table_def = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="pid", NAME=u"父ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="case_no", NAME=u"用例编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=False, ESSENTIAL=False),
            dict(ID="case_path", NAME=u"用例路径", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="case_name", NAME=u"用例名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="case_type", NAME=u"用例类型", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="case_desc", NAME=u"用例描述", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        self.title = u"选择用例"

        # Model
        self.__model = CaseSelModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = CaseSelControl(_table_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(_table_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButton()
        _wid_buttons.enable_search()
        _wid_buttons.enable_select()
        _wid_buttons.enable_cancel()
        _wid_buttons.create()

        # win_add
        self.__win_add = ViewAdd(_table_def)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_search.connect(self.__search)
        _wid_buttons.sig_select.connect(self.__select)
        _wid_buttons.sig_cancel.connect(self.close)

    def __search(self):
        self.__model.usr_search(self.__wid_search_cond.get_cond())

    def __select(self):
        _res = self.__model.usr_get_checked()
        self.sig_selected[dict].emit(_res)
        self.close()
