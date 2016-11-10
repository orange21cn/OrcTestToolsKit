# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import view_widget_def


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


class ViewWidgetDef(QWidget):

    sig_selected = OrcSignal(str)
    sig_search = OrcSignal()
    sig_delete = OrcSignal()

    def __init__(self, p_type=None):
        """
        支持选择类型,选择时按钮/查询条件/查询方式都有不同
        :param p_type:
        :return:
        """
        QWidget.__init__(self)

        self.__type = p_type

        # Model
        self.__model = WidgetDefModel()
        self.__model.usr_set_definition(view_widget_def)

        # Control
        _control = WidgetDefControl(view_widget_def)

        # Search
        if self.__type is not None:
            self.__wid_search_cond = ViewSearch(view_widget_def)
            self.__wid_search_cond.set_col_num(2)
            self.__wid_search_cond.create()
        else:
            self.__wid_search_cond = None

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons window
        btn_definition = []
        if self.__type is None:
            btn_definition.append(dict(id="add", name=u'增加')),
            btn_definition.append(dict(id="delete", name=u"删除"))
            btn_definition.append(dict(id="update", name=u"修改", type="CHECK"))
        btn_definition.append(dict(id="search", name=u"查询"))

        _wid_buttons = ViewButtons(btn_definition)
        _wid_buttons.align_back()

        # win_add
        self.__win_add = ViewAdd(view_widget_def)

        # Layout
        _layout = QVBoxLayout()
        if self.__type is not None:
            _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        # connection
        self.__win_add.sig_submit[dict].connect(self.add)
        _wid_buttons.sig_clicked.connect(self.__operate)

        if self.__type is None:
            _wid_display.clicked[QModelIndex].connect(self.__widget_detail)
        else:
            _wid_display.doubleClicked[QModelIndex].connect(self.__widget_detail)

    def __operate(self, p_flg):

        if "add" == p_flg:
            self.__win_add.show()

        elif "delete" == p_flg:
            self.__model.usr_delete()
            self.sig_delete.emit()

        elif "update" == p_flg:
            self.__model.usr_editable()

        elif "search" == p_flg:
            if self.__type is None:
                self.sig_search.emit()
            else:
                _cond = self.__wid_search_cond.get_cond()
                self.search(_cond)

        else:
            pass

    def search(self, p_cond):
        self.__model.usr_search(p_cond)

    def add(self, p_data):
        self.__model.usr_add(p_data)

    def __widget_detail(self, p_index):
        _widget_id = self.__model.usr_get_node(p_index).content["id"]
        self.sig_selected[str].emit(str(_widget_id))
