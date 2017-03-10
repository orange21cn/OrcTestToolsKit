# coding=utf-8
import json

from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QGridLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QPushButton
from PySide.QtGui import QWidget

from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck

from OrcView.Driver.Web.Page.PageDefView import PageDefView
from OrcView.Driver.Web.Widget.WidgetDefView import WidgetDefView
from OrcView.Lib.LibView import OrcLineEdit
from OrcView.Lib.LibView import OrcSelect
from OrcView.Lib.LibView import SelectWidgetOperation


class ViewOperate(QWidget):
    """

    """
    sig_submit = OrcSignal(str)

    def __init__(self):

        QWidget.__init__(self)

        self.__view_page_select = PageDefView('SINGLE')
        self.__view_widget_select = WidgetDefView('SINGLE')

        self.__operate_data = dict()

        # 主 layout
        _layout = QGridLayout()
        self.setLayout(_layout)

        # 控件类型
        _type_label = QLabel(u"对象类型")
        self.__type_select = OrcSelect('operate_object_type')

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
        self.__view_widget_select.sig_selected.connect(self.__set_widget)
        self.__view_page_select.sig_selected.connect(self.__set_page)
        self.__type_select.currentIndexChanged.connect(self.__change_type)

    def __submit(self):

        _data = dict(TYPE=self.__type_select.get_data(),
                     OBJECT=self.__operate_data["id"])

        if self.__operate_select.get_data() is not None:
            _data["OPERATION"] = self.__operate_select.get_data()

            if "INPUT" == _data["OPERATION"]:
                _data["DATA"] = ""

        self.sig_submit.emit(json.dumps(_data))
        self.close()

    def __set_widget(self, p_id):
        """
        :param p_id: widget id
        :return:
        """
        resource = OrcResource('WidgetDef')

        result = resource.get(path=p_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除控件"):
            return False

        self.__operate_data = result.data
        self.__widget_input.set_data(self.__operate_data['widget_path'])

        # 设置操作方式
        if "widget_type" in self.__operate_data:
            self.__operate_select.set_type(self.__operate_data["widget_type"])

    def __set_page(self, p_id):
        """
        设置界面
        :param p_id:
        :return:
        """
        resource = OrcResource('PageDef')

        result = resource.get(path=p_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除控件"):
            return False

        self.__operate_data = result.data
        self.__widget_input.set_data(self.__operate_data['page_flag'])

        # 设置操作方式
        self.__operate_select.set_type('PAGE')

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