# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibControl import LibControl

from OrcView.Data.DataAdd import ViewDataAdd
from OrcView.Driver.Web.WidgetSelect import ViewWidgetSelect
from CaseService import CaseDefService


class CaseDefModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self)

        i_base_url = 'http://localhost:5000/CaseDef'
        _interface = {
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url,
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class CaseDefControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewCaseDefMag(QWidget):

    sig_case_det = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        _table_def = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="pid", NAME=u"父ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="case_no", NAME=u"用例编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=False, ESSENTIAL=False),
            dict(ID="case_path", NAME=u"用例路径", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="case_name", NAME=u"用例名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="case_type", NAME=u"用例类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="case_desc", NAME=u"用例描述", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        self.title = u"用例管理"

        self.__service = CaseDefService()

        # Model
        self.__model = CaseDefModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = CaseDefControl(_table_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(_table_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Context menu
        _menu_def = [dict(NAME=u"增加", STR="sig_add"),
                     dict(NAME=u"删除", STR="sig_del"),
                     dict(NAME=u"增加数据", STR="sig_data"),
                     dict(NAME=u"添加至运行", STR="sig_run")]

        _wid_display.create_context_menu(_menu_def)

        # Buttons widget
        _wid_buttons = ViewButton()
        _wid_buttons.enable_add()
        _wid_buttons.enable_delete()
        _wid_buttons.enable_modify()
        _wid_buttons.enable_search()
        _wid_buttons.create()

        # win add case
        self.__win_add = ViewAdd(_table_def)

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
        _wid_buttons.sig_add.connect(self.__win_add.show)  # 弹出增加用例窗口
        _wid_buttons.sig_delete.connect(self.__model.usr_delete)  # 删除
        _wid_buttons.sig_modify.connect(self.__model.usr_editable)  # 设置可修改
        _wid_buttons.sig_search.connect(self.search)  # 查询

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
