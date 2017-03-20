# coding=utf-8
from functools import partial

from PySide.QtGui import QWidget
from PySide.QtGui import QGridLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QPushButton
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibView import create_editor
from OrcView.Lib.LibTheme import get_theme


class OrcButtons(QWidget):

    sig_clicked = OrcSignal(str)

    def __init__(self, p_def, p_direction="HOR", p_align="BACK"):
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
        if "HOR" == p_direction:
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
        if "BACK" == p_align:
            self.align_back()
        else:
            self.align_front()

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

    def __init__(self, p_def):
        """
        :param p_def: {id, name, type}
        :return:
        """
        QWidget.__init__(self)

        # 控件定义
        self.__fields_def = p_def

        # 每行默认控件数
        self.__columns = 4

        # 控件字典
        self.__inputs = {}

        # 布局
        self.__layout_srh = QGridLayout()
        self.setLayout(self.__layout_srh)

        self.setStyleSheet(get_theme("Input"))

    def set_col_num(self, p_num):
        """
        设置每行控件数
        :param p_num:
        :type p_num: int
        :return:
        """
        self.__columns = p_num

    def create(self):

        items = []

        for t_def in self.__fields_def:

            if not t_def['SEARCH']:
                continue

            # 控件标签
            _label = QLabel(t_def['NAME'] + ":")

            # 控件
            _def = dict(TYPE=t_def["TYPE"],
                        SOURCE="SEARCH",
                        FLAG=t_def["ID"])
            self.__inputs[t_def['ID']] = create_editor(_def)

            # 控件布局
            _layout = QHBoxLayout()
            _layout.addWidget(_label)
            _layout.addWidget(self.__inputs[t_def['ID']])

            items.append(_layout)

        # 控件及其 label 加入主布局
        for _index in range(len(items)):
            _row = _index % self.__columns
            _column = _index / self.__columns

            self.__layout_srh.addLayout(items[_index], _column, _row)

    def get_cond(self):
        """
        获取 条件
        :return: {name:value, ...}
        """
        return {_inp: self.__inputs[_inp].get_data() for _inp in self.__inputs}
