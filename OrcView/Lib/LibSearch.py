# coding=utf-8
from functools import partial

from PySide.QtGui import QWidget
from PySide.QtGui import QGridLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QPushButton
from PySide.QtCore import Signal as OrcSignal

from OrcLib.LibProgram import OrcFactory
from OrcLib.LibType import DirType
from OrcView.Lib.LibView import WidgetFactory
from OrcView.Lib.LibView import OrcRow
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibViewDef import WidgetDefinition


class OrcButtons(QWidget):

    sig_clicked = OrcSignal(str)

    def __init__(self, p_def, p_direction=DirType.HORIZON, p_align=DirType.BACK):
        """
        生成一个按钮组
        :param p_def: [{id, name, type=None}]
        :return: None
        """
        QWidget.__init__(self)

        # 定义
        self.__definition = p_def

        # 按钮字典
        self.__buttons = dict()

        # 设置方向
        if DirType.HORIZON == p_direction:
            self.__layout = QHBoxLayout()
        else:
            self.__layout = QVBoxLayout()

        # 设置 layout
        self.setLayout(self.__layout)

        # 添加按钮
        for t_def in self.__definition:

            _id = t_def["id"]
            _name = t_def["name"]
            _type = None if "type" not in t_def else t_def["type"]

            _button = QPushButton(_name)

            # Toggle button
            if _type is not None and "CHECK" == _type:
                _button.setCheckable(True)

            _button.clicked.connect(partial(self.sig_clicked.emit, _id))

            self.__buttons[_id] = _button
            self.__layout.addWidget(_button)

        # 默认向右对齐
        if DirType.BACK == p_align:
            self.align_back()
        elif DirType.FRONT:
            self.align_front()
        else:
            pass

        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)

        # 设置样式
        self.setStyleSheet(get_theme("Buttons"))

    def align_back(self):
        """
        向下/向右对齐
        :return:
        """
        self.__layout.insertStretch(0)

    def align_front(self):
        """
        向下/向左对齐
        :return:
        """
        self.__layout.addStretch()

    def set_disable(self, p_id):
        """
        设置按钮不可用
        :param p_id:
        :return:
        """
        if p_id in self.__buttons:
            self.__buttons[p_id].setEnabled(False)

    def set_enable(self, p_id):
        """
        设置按钮可用
        :param p_id:
        :return:
        """
        if p_id in self.__buttons:
            self.__buttons[p_id].setEnabled(True)

    def get_status(self, p_id):
        """
        获取按钮状态
        :param p_id:
        :return:
        """
        return self.__buttons[p_id].isChecked()


class ViewSearch(QWidget):
    """
    Search widget
    """
    def __init__(self, p_def, p_num=None):
        """
        :param p_def: {id, name, type}
        :return:
        """
        QWidget.__init__(self)

        # 可以输入字段类,或者标识
        if isinstance(p_def, WidgetDefinition):
            self._def = p_def
        else:
            self._def = WidgetDefinition(p_def)

        # 每行默认控件数
        self._columns = 4 if p_num is None else p_num

        # 控件字典
        self._conditions = OrcFactory.create_ordered_dict()

        # 生成控件字典
        for _key in self._def.search_keys:

            _field = self._def.field(_key)

            # 控件
            _widget_def = dict(TYPE=_field.type, SOURCE="SEARCH", FLAG=_field.id)
            _widget = OrcRow(_field.name + ":", WidgetFactory.create_widget(_widget_def))

            self._conditions.append(_field.id, _widget)

        # 布局
        self._layout_main = QGridLayout()

        # 控件及其 label 加入主布局
        for _index in range(self._def.length_search):
            _row = _index % self._columns
            _column = _index / self._columns

            self._layout_main.addLayout(self._conditions.value_by_index(_index), _column, _row)

        self.setLayout(self._layout_main)

        # 样式
        self._layout_main.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(get_theme("Input"))

    def get_cond(self):
        """
        获取 条件
        :return: {name:value, ...}
        """
        return {_key: self._conditions.value(_key).get_data() for _key in self._conditions.keys()}
