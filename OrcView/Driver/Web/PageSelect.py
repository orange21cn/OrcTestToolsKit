# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibSearch import ViewSearch


class PageSelectModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

        i_base_url = 'http://localhost:5000/PageDef'
        _interface = {
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url,
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class PageSelectControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewPageSelectMag(QWidget):

    sig_selected = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        _table_def = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="page_flag", NAME=u"页面标识", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="page_desc", NAME=u"页面描述", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        self.title = u"用例管理"

        # Model
        self.__model = PageSelectModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = PageSelectControl(_table_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(_table_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButton()
        _wid_buttons.enable_search()
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
        _wid_buttons.sig_search.connect(self.search)
        _wid_display.doubleClicked.connect(self.select)

    def search(self):
        _cond = self.__wid_search_cond.get_cond()
        self.__model.usr_search(_cond)

    def select(self, p_index):

        _node = self.__model.usr_get_data(p_index.row())
        _id = _node["id"]
        _flag = _node["page_flag"]

        self.sig_selected.emit(dict(id=str(_id), flag=_flag))

        self.close()
