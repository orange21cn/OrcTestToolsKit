# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibControl import LibControl


class PageDefModel(ModelTable):

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


class PageDefControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewPageDefMag(QWidget):

    sig_selected = OrcSignal(str)
    sig_search = OrcSignal()
    sig_delete = OrcSignal()

    def __init__(self, p_def):

        QWidget.__init__(self)

        _table_def = p_def

        self.title = u"用例管理"

        # Model
        self.__model = PageDefModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = PageDefControl(_table_def)

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
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_add.connect(self.__win_add.show)
        _wid_buttons.sig_delete.connect(self.__model.usr_delete)
        _wid_buttons.sig_delete.connect(self.sig_delete.emit)
        _wid_buttons.sig_modify.connect(self.__model.usr_editable)
        _wid_buttons.sig_search.connect(self.sig_search.emit)

        self.__win_add.sig_submit[dict].connect(self.add)
        _wid_display.clicked[QModelIndex].connect(self.__page_detail)

    def search(self, p_cond):
        self.__model.usr_search(p_cond)

    def add(self, p_data):
        self.__model.usr_add(p_data)

    def __page_detail(self, p_index):
        _page_id = self.__model.usr_get_data(p_index.row())["id"]
        self.sig_selected[str].emit(str(_page_id))
