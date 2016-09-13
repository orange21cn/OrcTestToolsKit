# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibControl import LibControl
from OrcView.Case.CaseSelect import ViewCaseSelMag


class BatchDetModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

        i_base_url = 'http://localhost:5000/BatchDet'
        _interface = {
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url,
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class BatchDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewBatchDetMag(QWidget):

    def __init__(self, p_data):

        QWidget.__init__(self)

        _table_def = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="case_id", NAME=u"用例ID", TYPE="LINETEXT", DISPLAY=False, EDIT=True,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="case_no", NAME=u"用例编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="case_name", NAME=u"用例名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        _batch_no = p_data["no"]
        self.__batch_id = p_data["id"]
        self.title = _batch_no

        # Model
        self.__model = BatchDetModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = BatchDetControl(_table_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(_table_def)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButton()
        _wid_buttons.enable_add()
        _wid_buttons.enable_delete()
        _wid_buttons.enable_search()
        _wid_buttons.create()

        # win_add
        self.__win_add = ViewCaseSelMag()

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_add.connect(self.__win_add.show)
        _wid_buttons.sig_delete.connect(self.__model.usr_delete)
        _wid_buttons.sig_search.connect(self.search)

        self.__win_add.sig_selected.connect(self.add)

    def search(self):
        _cond = self.__wid_search_cond.get_cond()
        _cond["batch_id"] = self.__batch_id
        self.__model.usr_search(_cond)

    def add(self, p_data):
        _data = {"batch_id": self.__batch_id, "case": p_data}
        self.__model.usr_add(_data)
