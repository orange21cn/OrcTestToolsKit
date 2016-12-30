# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QWidget
from PySide.QtGui import QLabel
from PySide.QtGui import QTabWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QGridLayout
from PySide.QtGui import QPushButton

from OrcView.Driver.Web.PageMain import PageContainer
from OrcView.Driver.Web.WidgetMain import WidgetContainer
from OrcView.Driver.Web.WindowDef import ViewWindow

from OrcView.Lib.LibView import OrcSelect
from OrcView.Lib.LibView import OrcLineEdit
from OrcView.Lib.LibView import OrcTextArea
from OrcView.Lib.LibView import SelectWidgetType
from OrcView.Lib.LibView import SelectWidgetOperation
from OrcView.Lib.LibDict import LibDict
from OrcView.Lib.LibTheme import get_theme

from WebService import WebMainService


class ViewWebMain(QWidget):
    """

    """
    sig_page_selected = OrcSignal(str)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"Web对象管理"

        # Page
        _page = PageContainer()

        # Window
        _window = ViewWindow()

        # Widget
        _widget = WidgetContainer()

        # 页面 tab
        _tab = QTabWidget()
        _tab.addTab(_page, _page.title)
        _tab.addTab(_window, _window.title)
        _tab.addTab(_widget, _widget.title)

        _tab.setTabPosition(QTabWidget.West)
        _tab.setStyleSheet(get_theme("TabViewWeb"))

        # 测试区
        self.__test = WidgetTest()
        self.__test.setStyleSheet(get_theme("TestWidget"))

        # 主layout
        _layout = QHBoxLayout()
        _layout.addWidget(_tab)
        _layout.addWidget(self.__test)

        _layout.setStretch(0, 5)
        _layout.setStretch(1, 1)

        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.setSpacing(0)

        self.setLayout(_layout)

        # 信号
        _page.sig_selected.connect(self.set_page)
        _widget.sig_selected.connect(self.set_widget)
        self.__test.sig_exec.connect(self.send)

    def set_page(self, p_id):
        self.__test.set_type("PAGE", p_id)

    def set_widget(self, p_id):
        self.__test.set_type("WIDGET", p_id)

    def send(self):
        # Todo 接口调用方式
        _data = dict(OBJECT=self.__test.id,
                     TYPE=self.__test.type,
                     ENV=self.__test.env,
                     OPERATION=self.__test.operation,
                     DATA=self.__test.data,
                     BROWSER="FIREFOX")

        from OrcLib.LibNet import OrcSocketResource

        _resource = OrcSocketResource("DriverWeb")

        _result = _resource.get(_data)
        self.__test.set_status(_result)


class WidgetTest(QWidget):

    sig_exec = OrcSignal()

    def __init__(self):

        QWidget.__init__(self)

        self.__dict = LibDict()
        self.__service = WebMainService()

        self.id = None
        self.type = None
        self.operation = None
        self.data = None
        self.env = None

        # 输入框
        _layout_top = QGridLayout()

        self.__edit_type = OrcSelect()  # 类型,页面或者控件
        self.__edit_flag = OrcLineEdit()  # 标识符
        self.__widget_type = SelectWidgetType(True)  # 控件类型
        self.__widget_ope = SelectWidgetOperation(True)  # 控件操作类型
        self.__widget_data = OrcLineEdit()

        self.__edit_type.set_empty()
        self.__edit_type.set_flag("operate_object_type")
        self.__edit_type.setEnabled(False)
        self.__edit_flag.setEnabled(False)
        self.__widget_type.setEnabled(False)
        self.__widget_data.setEnabled(False)

        _layout_top.addWidget(QLabel(u"类型:"), 0, 0)
        _layout_top.addWidget(self.__edit_type, 0, 1)
        _layout_top.addWidget(QLabel(u"标识:"), 1, 0)
        _layout_top.addWidget(self.__edit_flag, 1, 1)
        _layout_top.addWidget(QLabel(u"控件:"), 2, 0)
        _layout_top.addWidget(self.__widget_type, 2, 1)
        _layout_top.addWidget(QLabel(u"操作:"), 3, 0)
        _layout_top.addWidget(self.__widget_ope, 3, 1)
        _layout_top.addWidget(QLabel(u"数据:"), 4, 0)
        _layout_top.addWidget(self.__widget_data, 4, 1)

        self.__edit_status = OrcTextArea(self)
        self.__edit_status.setReadOnly(True)

        # 按钮
        _layout_button = QHBoxLayout()

        self.__btn_exec = QPushButton(u"执行")
        self.__btn_exec.setStyleSheet(get_theme("Buttons"))

        _layout_button.addStretch()
        _layout_button.addWidget(self.__btn_exec)

        # 主界面
        _layout = QVBoxLayout()
        _layout.addLayout(_layout_top)
        _layout.addWidget(self.__edit_status)
        _layout.addLayout(_layout_button)

        self.setLayout(_layout)

        self.__widget_ope.currentIndexChanged.connect(self.__set_operation)
        self.__widget_data.textChanged.connect(self.__set_data)
        self.__btn_exec.clicked.connect(self.sig_exec.emit)

    def __set_operation(self):

        _ope = self.__widget_ope.get_data()

        if not _ope:
            self.operation = None
        else:
            self.operation = _ope

    def __set_data(self):
        self.data = self.__widget_data.get_data()

    def set_type(self, p_type, p_id):

        # 设置对象类型
        _type_text = self.__dict.get_dict("operate_object_type", p_type)[0].dict_text
        self.__edit_type.set_data(_type_text)

        self.id = p_id
        self.type = p_type

        if "PAGE" == p_type:

            _page_id, _page_flg, _page_env = self.__service.get_page_key(p_id)
            _page_key = "%s[%s]" % (_page_flg, _page_env)

            self.id = _page_id
            self.env = _page_env

            # 设置页面标识
            self.__edit_flag.set_data(_page_key)

            # 禁用控件类型
            self.__widget_type.set_data("")

            # 页面操作项
            self.__widget_ope.set_type("PAGE")
            # self.__widget_ope.setEnabled(False)

            # 禁止输入数据
            self.__widget_data.clear()
            self.__widget_data.setEnabled(False)

        elif "WIDGET" == p_type:

            _widget_key = self.__service.get_widget_key(p_id)
            _widget_type = self.__service.get_widget_type(p_id)

            # 设置控件标识
            self.__edit_flag.set_data(_widget_key)

            # 设置控件类型
            self.__widget_type.set_data(_widget_type)

            # 重置控件操作项
            self.__widget_ope.set_type(_widget_type)
            # self.__widget_ope.setEnabled(True)

            # 数据输入框可用
            self.__widget_data.setEnabled(True)

        else:
            pass

    def set_env(self, p_env):
        self.env = p_env

    def set_status(self, p_data):

        self.__edit_status.setText(p_data)
