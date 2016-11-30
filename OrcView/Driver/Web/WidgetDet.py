# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelNewTable
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import def_view_widget_det

from WidgetService import WidgetDetService


class WidgetDetModel(ModelNewTable):

    def __init__(self):

        ModelNewTable.__init__(self)

        self.usr_set_service(WidgetDetService())


class WidgetDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewWidgetDetMag(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        # Current widget id
        self.__widget_id = None

        # Model
        self.__model = WidgetDetModel()
        self.__model.usr_set_definition(def_view_widget_det)

        # Control
        _control = WidgetDetControl(def_view_widget_det)

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
        self.__win_add = ViewAdd(def_view_widget_det)

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)

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

    def __operate(self, p_flag):

        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.__model.usr_delete()
        elif "update" == p_flag:
            self.__model.usr_editable()
        else:
            pass
