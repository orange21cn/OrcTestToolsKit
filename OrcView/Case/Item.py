# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QWidget
from PySide.QtGui import QPushButton
from PySide.QtGui import QLabel
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QGridLayout

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibView import OrcSelect
from OrcView.Lib.LibView import OrcLineEdit
from OrcView.Lib.LibView import SelectWidgetOperation
from OrcView.Lib.LibViewDef import def_view_item
from OrcView.Data.DataAdd import ViewDataAdd
from OrcView.Driver.Web.WidgetSelect import ViewWidgetSelect
from OrcView.Driver.Web.PageSelect import ViewPageSelectMag
from StepService import ItemService
from StepService import StepService
from CaseSelect import ViewCaseSelMag


class ItemModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self)
        self.usr_set_service(ItemService())


class ItemControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ItemView(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.__step_id = None
        self.__service_step_def = StepService()

        # Current case id
        self.__step_type = None
        self.__win_operate = ViewOperate()

        # Model
        self.__model = ItemModel()
        self.__model.usr_set_definition(def_view_item)

        # Control
        _control = ItemControl(def_view_item)

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
        _wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="up", name=u"上移"),
            dict(id="down", name=u"下移"),
        ], "VER")

        # 新增 item 窗口
        self.__win_add_item = ViewAdd(def_view_item)

        # 新增 func 窗口
        self.__win_add_func = ViewCaseSelMag("SINGLE")

        # win add data
        self.__win_data = ViewDataAdd()

        # Layout
        _layout = QHBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        # Connection
        self.__win_add_item.sig_operate.connect(self.__win_operate.show)  # 显示操作选择框
        self.__win_add_item.sig_submit.connect(self.add_item)  # 新增
        self.__win_add_func.sig_selected.connect(self.add_func)  # 新增
        self.__win_operate.sig_submit.connect(self.get_operate)
        _wid_buttons.sig_clicked.connect(self.__operate)  # 按钮点击
        _wid_display.sig_context.connect(self.__context)  # 右键菜单
        _wid_display.clicked.connect(self.__model.usr_set_current_data)  # 单击

    def add_show(self):

        if self.__step_id is not None:

            _type = self.__service_step_def.view_get_step_type(self.__step_id)

            if "FUNC" == _type:
                self.__win_add_func.show()
            elif "NORMAL" == _type:
                self.__win_add_item.show()
            else:
                pass

    def add_item(self, p_data):

        _data = dict(
            type="ITEM",
            step_id=self.__step_id,
            data=p_data
        )
        self.__model.usr_add(_data)

    def add_func(self, p_data):

        _data = dict(
            type="FUNC",
            step_id=self.__step_id,
            data=p_data[0],
        )
        self.__model.usr_add(_data)

    def set_step_id(self, p_step_id):

        self.__step_id = p_step_id
        self.__model.usr_search({"step_id": self.__step_id})

    def clean(self):
        self.__step_id = None
        self.__model.usr_clean()

    def __operate(self, p_flag):

        if "add" == p_flag:
            self.add_show()
        elif "delete" == p_flag:
            self.__model.usr_delete()
        elif "update" == p_flag:
            self.__model.usr_editable()
        elif "up" == p_flag:
            self.__model.usr_up()
        elif "down" == p_flag:
            self.__model.usr_down()
        else:
            pass

    def __context(self, p_flag):

        if "sig_data" == p_flag:

            _path = self.__model.usr_get_current_data()["item_no"]
            self.__win_data.show()
            self.__win_data.set_type("ITEM")
            self.__win_data.set_id(_path)

    def get_operate(self, p_data):
        # self. Todo
        self.__win_add_item.set_data("item_operate", p_data)


class ViewOperate(QWidget):
    """

    """
    sig_submit = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        self.__view_page_select = ViewPageSelectMag()
        self.__view_widget_select = ViewWidgetSelect()

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
        _layout.addWidget(self.__widget_input, 1, 1)
        _layout.addWidget(_operate_label, 2, 0)
        _layout.addWidget(self.__operate_select, 2, 1)
        _layout.addLayout(_layout_button, 3, 1)

        self.__change_type("PAGE")

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

            if "INPUT" == _data["OPERATION"]:
                _data["DATA"] = ""

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
            self.__operate_select.set_type(_type)
        elif"PAGE" == _type:
            self.__operate_select.set_type("PAGE")
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


class OperationDict:
    """
    Todo
    """
    def __init__(self):

        self.object = None
        self.operation = None
        self.data = None
        self.attr = None
