# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import LibControl


class WidgetDefModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self)

        _base_url = 'http://localhost:5000/WidgetDef'
        _interface = {
            'usr_add': '%s/usr_add' % _base_url,
            'usr_delete': '%s/usr_delete' % _base_url,
            'usr_modify': '%s/usr_modify' % _base_url,
            'usr_search': '%s/usr_search_all' % _base_url
        }

        self.usr_set_interface(_interface)


class WidgetDefControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewWidgetDefMag(QWidget):

    sig_selected = OrcSignal(str)
    sig_search = OrcSignal()
    sig_delete = OrcSignal()

    def __init__(self, p_def):

        QWidget.__init__(self)

        _table_def = p_def

        # Model
        self.__model = WidgetDefModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = WidgetDefControl(_table_def)

        # Data result display widget
        _wid_display = ViewTree()
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
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_add.connect(self.__win_add.show)
        _wid_buttons.sig_delete.connect(self.__model.usr_delete)
        _wid_buttons.sig_delete.connect(self.sig_delete.emit)
        _wid_buttons.sig_modify.connect(self.__model.usr_editable)
        _wid_buttons.sig_search.connect(self.sig_search.emit)

        self.__win_add.sig_submit[dict].connect(self.add)
        _wid_display.clicked[QModelIndex].connect(self.__widget_detail)

    def search(self, p_cond):
        self.__model.usr_search(p_cond)

    def add(self, p_data):
        self.__model.usr_add(p_data)

    def __widget_detail(self, p_index):
        _widget_id = self.__model.usr_get_node(p_index).content["id"]
        self.sig_selected[str].emit(str(_widget_id))
