# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import def_view_case_def

from OrcView.Data.DataAdd import ViewDataAdd
from OrcView.Driver.Web.WidgetSelect import ViewWidgetSelect

from CaseService import CaseDefService


class CaseDefModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self)
        self.usr_set_service(CaseDefService())


class CaseDefControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewCaseDefMag(QWidget):

    sig_case_det = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"用例管理"

        self.__service = CaseDefService()

        # Model
        self.__model = CaseDefModel()
        self.__model.usr_set_definition(def_view_case_def)

        # Control
        _control = CaseDefControl(def_view_case_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_case_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Context menu
        _wid_display.create_context_menu([
            dict(NAME=u"增加", STR="sig_add"),
            dict(NAME=u"删除", STR="sig_del"),
            dict(NAME=u"增加数据", STR="sig_data"),
            dict(NAME=u"添加至运行", STR="sig_run")])

        # Buttons widget
        _wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="search", name=u"查询")
        ])

        # win add case
        self.__win_add = ViewAdd(def_view_case_def)

        # 选择控件
        self.__win_widget_select = ViewWidgetSelect()

        # win add data
        self.__win_data = ViewDataAdd()

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)

        self.__win_add.sig_submit[dict].connect(self.add)  # 增加用例
        _wid_display.doubleClicked[QModelIndex].connect(self.__case_detail)  # 打开用例详情窗

        _wid_display.sig_context.connect(self.__context)  # 右键菜单
        _wid_display.clicked.connect(self.__model.usr_set_current_data)

        self.__win_data.widgets["data_flag"]["WIDGET"].clicked.connect(self.__win_widget_select.show)
        self.__win_widget_select.sig_selected.connect(self.set_widget)

    def set_widget(self, p_data):
        self.__win_data.set_data("data_flag", p_data["id"])

    def search(self):
        """
        查询
        :return:
        """
        self.__model.usr_search(self.__wid_search_cond.get_cond())

    def add(self, p_data):
        """
        增加用例
        :param p_data:
        :return:
        """
        self.__model.usr_add(p_data)

    def __operate(self, p_flag):

        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.__model.usr_delete()
        elif "update" == p_flag:
            self.__model.usr_editable()
        elif "search" == p_flag:
            self.search()
        else:
            pass

    def __case_detail(self, p_index):

        if not self.__model.usr_get_editable():

            _id = self.__model.usr_get_node(p_index).content["id"]
            _no = self.__model.usr_get_node(p_index).content["case_no"]
            _data = {"id": _id, "no": _no}

            self.sig_case_det[dict].emit(_data)

    def __context(self, p_flag):

        if "sig_data" == p_flag:

            _path = self.__model.usr_get_current_data().content["case_path"]
            _id = self.__model.usr_get_current_data().content["id"]

            self.__win_data.show()
            self.__win_data.set_type("CASE")
            self.__win_data.set_path(_path)
            self.__win_data.set_id(_id)
            # self.__win_data.set_enable("data_flag", False)

        elif "sig_run" == p_flag:

            case_id = self.__model.usr_get_current_data().content["id"]
            self.__service.add_to_run(case_id)
