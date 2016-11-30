# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelNewTable
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import def_view_batch_det
from OrcView.Case.CaseSelect import ViewCaseSelMag
from BatchService import BatchDetService

class BatchDetModel(ModelNewTable):

    def __init__(self):

        ModelNewTable.__init__(self)

        self.usr_set_service(BatchDetService())


class BatchDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewBatchDetMag(QWidget):

    def __init__(self, p_data):

        QWidget.__init__(self)

        _batch_no = p_data["no"]
        self.__batch_id = p_data["id"]
        self.title = _batch_no

        # Model
        self.__model = BatchDetModel()
        self.__model.usr_set_definition(def_view_batch_det)

        # Control
        _control = BatchDetControl(def_view_batch_det)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_batch_det)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="search", name=u"查询")
        ])

        # win_add
        self.__win_add = ViewCaseSelMag()

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)

        self.__win_add.sig_selected.connect(self.add)

    def search(self):
        _cond = self.__wid_search_cond.get_cond()
        _cond["batch_id"] = self.__batch_id
        self.__model.usr_search(_cond)

    def add(self, p_data):
        _data = {"batch_id": self.__batch_id, "case": p_data}
        self.__model.usr_add(_data)

    def __operate(self, p_flag):

        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.__model.usr_delete()
        elif "search" == p_flag:
            self.search()
        else:
            pass
