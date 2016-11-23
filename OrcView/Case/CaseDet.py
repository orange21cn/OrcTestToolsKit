# coding=utf-8

from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibViewDef import def_view_case_det
from OrcView.Data.DataAdd import ViewDataAdd


class CaseDetModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

        i_base_url = 'http://localhost:5000/CaseDet'
        _interface = {
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url,
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class CaseDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewCaseDetMag(QWidget):

    sig_select = OrcSignal(str)
    sig_search = OrcSignal()
    sig_delete = OrcSignal()

    def __init__(self, p_id):

        QWidget.__init__(self)

        self.__case_id = p_id

        # Model
        self.__model = CaseDetModel()
        self.__model.usr_set_definition(def_view_case_det)
        self.__model.usr_search({"case_id": self.__case_id})

        # Control
        _control = CaseDetControl(def_view_case_det)

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # 界面列宽自适应
        _wid_display.resizeColumnsToContents()

        # Context menu
        _menu_def = [dict(NAME=u"增加", STR="sig_add"),
                     dict(NAME=u"删除", STR="sig_del"),
                     dict(NAME=u"增加数据", STR="sig_data")]

        _wid_display.create_context_menu(_menu_def)

        # Buttons widget
        _wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK")
        ], "VER")

        # win_add
        self.__win_add = ViewAdd(def_view_case_det)

        # win add data
        self.__win_data = ViewDataAdd()

        # Layout
        _layout = QHBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)

        _wid_display.clicked.connect(self.__selected)
        self.__win_add.sig_submit.connect(self.add)

        _wid_display.sig_context.connect(self.__context)  # 右键菜单
        _wid_display.clicked.connect(self.__model.usr_set_current_data)

    def add(self, p_data):

        _data = {"case_det": {"case_id": self.__case_id}, "step": p_data}
        self.__model.usr_add(_data)

    def __operate(self, p_flag):

        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.__model.usr_delete()
            self.sig_delete.emit()
        elif "update" == p_flag:
            self.__model.usr_editable()
        else:
            pass

    def __selected(self, p_index):

        _index = p_index.row()
        _step_id = self.__model.usr_get_data(_index)["step_id"]

        self.sig_select.emit(str(_step_id))

    def __context(self, p_flag):

        if "sig_data" == p_flag:

            _path = self.__model.usr_get_current_data()["step_no"]
            self.__win_data.show()
            self.__win_data.set_type("STEP")
            self.__win_data.set_id(_path)
