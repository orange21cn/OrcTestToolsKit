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


class WidgetDetModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

        i_base_url = 'http://localhost:5000/WidgetDet'
        _interface = {
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url,
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class WidgetDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewWidgetDetMag(QWidget):

    def __init__(self, p_def):

        QWidget.__init__(self)

        _table_def = p_def

        # Current widget id
        self.__widget_id = None

        # Model
        self.__model = WidgetDetModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = WidgetDetControl(_table_def)

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

        self.__win_add.sig_submit[dict].connect(self.add)

    def add_show(self):

        if self.__widget_id is not None:
            self.__win_add.show()

    def add(self, p_data):
        _data = p_data
        _data["widget_id"] = self.__widget_id
        self.__model.usr_add(_data)

    def set_widget_id(self, p_widget_id):
        self.__widget_id = p_widget_id
        self.__model.usr_search({"widget_id": self.__widget_id})

    def clean(self):
        self.__widget_id = None
        self.__model.usr_clean()
