# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import LibControl


class PageDetModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

        i_base_url = 'http://localhost:5000/PageDet'
        _interface = {
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url,
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class PageDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewPageDetMag(QWidget):
    """

    """
    sig_selected = OrcSignal(str)

    def __init__(self, p_def):

        QWidget.__init__(self)

        _table_def = p_def

        # Current page id
        self.__page_id = None

        # Model
        self.__model = PageDetModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = PageDetControl(_table_def)

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons widget
        _wid_buttons = ViewButton()
        _wid_buttons.enable_add()
        _wid_buttons.enable_delete()
        _wid_buttons.enable_modify()
        _wid_buttons.create()

        # win_add
        self.__win_add = ViewAdd(_table_def)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_add.connect(self.add_show)
        _wid_buttons.sig_delete.connect(self.__model.usr_delete)
        _wid_buttons.sig_modify.connect(self.__model.usr_editable)
        _wid_display.clicked[QModelIndex].connect(self.__page_select)

        self.__win_add.sig_submit[dict].connect(self.add)

    def __page_select(self, p_index):
        _id = self.__model.usr_get_data(p_index.row())["id"]
        self.sig_selected.emit(_id)

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
