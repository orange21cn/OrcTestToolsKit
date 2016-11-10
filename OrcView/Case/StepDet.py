# coding=utf-8
import json

from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QWidget
from PySide.QtGui import QPushButton
from PySide.QtGui import QLabel
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QGridLayout

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibView import OrcSelect
from OrcView.Lib.LibView import OrcLineEdit
from OrcView.Lib.LibView import SelectWidgetOperation
from OrcView.Data.DataAdd import ViewDataAdd
from OrcView.Driver.Web.WidgetSelect import ViewWidgetSelectMag
from OrcView.Driver.Web.PageSelect import ViewPageSelectMag


class StepDetModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)

        i_base_url = 'http://localhost:5000/StepDet'
        _interface = {
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url,
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class StepDetControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewStepDetMag(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        _table_def = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="item_no", NAME=u"条目编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=False, ESSENTIAL=False),
            dict(ID="item_type", NAME=u"条目类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="item_mode", NAME=u"条目模式", TYPE="SELECT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="item_operate", NAME=u"条目操作", TYPE="OPERATE", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="item_desc", NAME=u"条目描述", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        # Current case id
        self.__step_id = None
        self.__win_operate = ViewOperate()

        # Model
        self.__model = StepDetModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = StepDetControl(_table_def)

        # Data result display widget
        _wid_display = ViewTable()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Context menu
        _menu_def = [dict(NAME=u"增加", STR="sig_add"),
                     dict(NAME=u"删除", STR="sig_del"),
                     dict(NAME=u"增加数据", STR="sig_data")]

        _wid_display.create_context_menu(_menu_def)

        # Buttons widget
        _wid_buttons = ViewButton("VER")
        _wid_buttons.enable_add()
        _wid_buttons.enable_delete()
        _wid_buttons.enable_modify()
        _wid_buttons.create()

        # win_add
        self.__win_add = ViewAdd(_table_def)
        self.__win_add.sig_operate.connect(self.__win_operate.show)
        self.__win_operate.sig_submit.connect(self.get_operate)

        # win add data
        self.__win_data = ViewDataAdd()

        # Layout
        _layout = QHBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_add.connect(self.add_show)
        _wid_buttons.sig_delete.connect(self.__model.usr_delete)
        _wid_buttons.sig_modify.connect(self.__model.usr_editable)

        self.__win_add.sig_submit.connect(self.add)

        _wid_display.sig_context.connect(self.__context)  # 右键菜单
        _wid_display.clicked.connect(self.__model.usr_set_current_data)

    def add_show(self):
        if self.__step_id is not None:
            self.__win_add.show()

    def add(self, p_data):
        _data = p_data
        _data["step_id"] = self.__step_id
        self.__model.usr_add(_data)

    def set_step_id(self, p_step_id):
        self.__step_id = p_step_id
        self.__model.usr_search({"step_id": self.__step_id})

    def clean(self):
        self.__step_id = None
        self.__model.usr_clean()

    def __context(self, p_flag):

        if "sig_data" == p_flag:

            _path = self.__model.usr_get_current_data()["item_no"]
            self.__win_data.show()
            self.__win_data.set_type("ITEM")
            self.__win_data.set_id(_path)

    def get_operate(self, p_data):
        # self. Todo
        print p_data
        self.__win_add.set_data("item_operate", p_data)


class ViewOperate(QWidget):
    """

    """
    sig_submit = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        self.__view_page_select = ViewPageSelectMag()
        self.__view_widget_select = ViewWidgetSelectMag()

        self.__widget_data = dict()

        # 主 layout
        _layout = QGridLayout()
        self.setLayout(_layout)

        # 控件类型
        _type_label = QLabel(u"对象类型")
        self.__type_select = OrcSelect("operate_object_type")

        # 控件信息输入
        _widget_label = QLabel(u"控件")
        self.__widget_input = OrcLineEdit()
        self.__widget_input.setReadOnly(True)

        # 控件输入 layout
        _layout_widget = QHBoxLayout()
        _layout_widget.addWidget(self.__widget_input)

        # 操作信息输入 layout
        _operate_label = QLabel(u"操作")
        self.__operate_select = SelectWidgetOperation()

        # 按钮
        _button_submit = QPushButton(u"确定")
        _button_cancel = QPushButton(u"取消")

        # 按钮 layout
        _layout_button = QHBoxLayout()
        _layout_button.addStretch()
        _layout_button.addWidget(_button_submit)
        _layout_button.addWidget(_button_cancel)

        _layout.addWidget(_type_label, 0, 0)
        _layout.addWidget(self.__type_select, 0, 1)
        _layout.addWidget(_widget_label, 1, 0)
        _layout.addLayout(_layout_widget, 1, 1)
        _layout.addWidget(_operate_label, 2, 0)
        _layout.addWidget(self.__operate_select, 2, 1)
        _layout.addLayout(_layout_button, 3, 1)

        self.__change_type(0)

        # connection
        _button_cancel.clicked.connect(self.close)
        _button_submit.clicked.connect(self.__submit)
        self.__widget_input.clicked.connect(self.__show_select)
        self.__view_widget_select.sig_selected[dict].connect(self.__set_widget)
        self.__view_page_select.sig_selected[dict].connect(self.__set_widget)
        self.__type_select.currentIndexChanged.connect(self.__change_type)

    def __submit(self):

        _data = dict(TYPE=self.__type_select.get_data(),
                     OBJECT=self.__widget_data["id"])

        if self.__operate_select.get_data() is not None:
            _data["OPERATION"] = self.__operate_select.get_data()

        self.sig_submit[dict].emit(_data)
        self.close()

    def __set_widget(self, p_data):
        """
        :param p_data: {'flag': u'dddd', 'type': u'WINDOW', 'id': '3300000002'}
        :return:
        """
        self.__widget_data = p_data
        self.__widget_input.set_data(p_data["flag"])

        # 设置操作方式
        if "type" in p_data:
            self.__operate_select.set_type(p_data["type"])

    def __change_type(self, p_data):

        _type = self.__type_select.get_data()

        self.__widget_input.clear()

        if "WIDGET" == _type:
            self.__operate_select.set_type("widget_operator")
        elif"PAGE" == _type:
            self.__operate_select.set_type("page_operator")
        else:
            self.__operate_select.set_type("")

    def __show_select(self):
        """
        Show a select widget according to type
        :return:
        """
        _type = self.__type_select.get_data()

        if "WIDGET" == _type:
            self.__view_widget_select.show()
        else:
            self.__view_page_select.show()


class ViewCheck(QWidget):
    """

    """
    def __init__(self):

        QWidget.__init__(self)

        self.__test = QPushButton("ViewCheck")

        _layout = QVBoxLayout()
        self.setLayout(_layout)

        _layout.addWidget(self.__test)
