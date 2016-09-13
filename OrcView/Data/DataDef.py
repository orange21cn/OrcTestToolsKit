# coding=utf-8

from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibAdd import ViewAdd

from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibControl import LibControl


_data_def = [dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                  SEARCH=False, ADD=False, ESSENTIAL=False),
             dict(ID="src_type", NAME=u"数据源类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
                  SEARCH=True, ADD=True, ESSENTIAL=True),
             dict(ID="src_id", NAME=u"数据源标识", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                  SEARCH=True, ADD=True, ESSENTIAL=True),
             dict(ID="data_flag", NAME=u"数据标识", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                  SEARCH=True, ADD=True, ESSENTIAL=True),
             dict(ID="data_order", NAME=u"数据顺序", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                  SEARCH=True, ADD=False, ESSENTIAL=False),
             dict(ID="data_mode", NAME=u"数据类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
                  SEARCH=True, ADD=True, ESSENTIAL=False),
             dict(ID="data_value", NAME=u"数据", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                  SEARCH=True, ADD=True, ESSENTIAL=False),
             dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                  SEARCH=False, ADD=True, ESSENTIAL=False),
             dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                  SEARCH=False, ADD=False, ESSENTIAL=False),
             dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                  SEARCH=False, ADD=False, ESSENTIAL=False)]


class DataModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

        i_base_url = 'http://localhost:5000/Data'
        _interface = {
            'usr_search': '%s/usr_search' % i_base_url,
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url
        }

        self.usr_set_interface(_interface)


class DataControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewDataMag(QWidget):
    """
    View of table
    """
    def __init__(self):

        QWidget.__init__(self)

        _table_def = _data_def

        self.title = u"数据管理"

        # Model
        self.__model = DataModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = DataControl(_table_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(_table_def)
        self.__wid_search_cond.set_col_num(3)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButton()
        _wid_buttons.enable_add()
        _wid_buttons.enable_delete()
        _wid_buttons.enable_modify()
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
        _wid_buttons.sig_add.connect(self.__win_add.show)
        _wid_buttons.sig_delete.connect(self.__model.usr_delete)
        _wid_buttons.sig_modify.connect(self.__model.usr_editable)
        _wid_buttons.sig_search.connect(self.search)

        self.__win_add.sig_submit[dict].connect(self.add)

    def search(self):

        self.__model.usr_search(self.__wid_search_cond.get_cond())

    def add(self, p_data):
        self.__model.usr_add(p_data)
