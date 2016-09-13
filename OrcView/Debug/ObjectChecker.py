# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QLabel
from PySide.QtGui import QPushButton
from PySide.QtGui import QTableView
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibView import OrcLineEdit
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibView import ObjectOperator


class ObjectChecker(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        # Top widget
        _object = QTableView()
        _object_property = DebugWidgetDef()

        _label_object = QLabel(u"对象")
        _label_object_property = QLabel(u"对象属性")

        _layout_object = QVBoxLayout()
        _layout_object.addWidget(_label_object)
        _layout_object.addWidget(_object)

        _layout_object_property = QVBoxLayout()
        _layout_object_property.addWidget(_label_object_property)
        _layout_object_property.addWidget(_object_property)

        # Top layout
        _layout_top = QHBoxLayout()
        _layout_top.addLayout(_layout_object)
        _layout_top.addLayout(_layout_object_property)

        # data widget
        _label_father = QLabel(u"父对象")
        _input_father = OrcLineEdit(self)
        _button_father = QPushButton("...")

        _layout_father = QHBoxLayout()
        _layout_father.addWidget(_label_father)
        _layout_father.addWidget(_input_father)
        _layout_father.addWidget(_button_father)

        _label_object_name = QLabel(u"对象名")
        _input_object_name = OrcLineEdit(self)

        _layout_object = QHBoxLayout()
        _layout_object.addWidget(_label_object_name)
        _layout_object.addWidget(_input_object_name)

        # data layout
        _layout_data = QVBoxLayout()
        _layout_data.addLayout(_layout_father)
        _layout_data.addLayout(_layout_object)

        # # property widget
        _operate = ObjectOperator()

        _layout_select = QHBoxLayout()
        _layout_select.addLayout(_layout_data)
        _layout_select.addLayout(_operate)
        _layout_select.setSpacing(1)
        _layout_select.setStretch(0, 1)
        _layout_select.setStretch(1, 1)

        # Bottom layout
        _layout_property = QHBoxLayout()

        # Button
        _btn_definition = [
            dict(id="btn_test", name=u"测试"),
            dict(id="btn_save", name=u"保存")
        ]
        _buttons = ViewButtons(_btn_definition)
        _buttons.align_back()

        _layout = QVBoxLayout()
        _layout.addLayout(_layout_top)
        _layout.addLayout(_layout_select)
        _layout.addLayout(_layout_property)
        _layout.addWidget(_buttons)

        self.setLayout(_layout)


class DebugWidgetDef(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        _table = QTableView()

        # 控件定义控件
        _btn_definition = [
            dict(id="add_def", name="+"),
            dict(id="delete_def", name="-"),
            dict(id="up_def", name=u"^"),
            dict(id="down_def", name=u"v")
        ]
        _buttons = ViewButtons(_btn_definition, "VERTICAL")
        _buttons.align_front()
        _buttons.set_no_spacing()

        _layout = QHBoxLayout()
        _layout.addWidget(_table)
        _layout.addWidget(_buttons)

        self.setLayout(_layout)
