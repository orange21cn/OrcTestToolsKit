# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelNewTable
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import def_view_page_det

from PageService import PageDetService


class PageDetModel(ModelNewTable):

    def __init__(self):

        ModelNewTable.__init__(self)

        self.usr_set_service(PageDetService())


class PageDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewPageDetMag(QWidget):
    """

    """
    sig_selected = OrcSignal(str)

    def __init__(self):

        QWidget.__init__(self)

        # Current page id
        self.__page_id = None

        # Model
        self.__model = PageDetModel()
        self.__model.usr_set_definition(def_view_page_det)

        # Control
        _control = PageDetControl(def_view_page_det)

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK")
        ])

        # win_add
        self.__win_add = ViewAdd(def_view_page_det)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)
        _wid_display.clicked[QModelIndex].connect(self.__page_select)

        self.__win_add.sig_submit[dict].connect(self.add)

    def __operate(self, p_flag):

        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.__model.usr_delete()
        elif "update" == p_flag:
            self.__model.usr_editable()
        else:
            pass

    def __page_select(self, p_index):
        page_det_id = self.__model.usr_get_data(p_index.row())["id"]
        self.sig_selected.emit(page_det_id)

    def add_show(self):
        if self.__page_id is not None:
            self.__win_add.show()

    def add(self, p_data):
        _data = p_data
        _data["page_id"] = self.__page_id
        self.__model.usr_add(_data)

    def set_page_id(self, p_page_id):
        self.__page_id = p_page_id
        self.__model.usr_search({"page_id": self.__page_id})

    def clean(self):
        self.__model.usr_clean()
