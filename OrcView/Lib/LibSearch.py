# coding=utf-8
from functools import partial

from PySide.QtGui import QWidget
from PySide.QtGui import QGridLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QPushButton
from PySide.QtCore import SIGNAL
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibView import create_editor
from OrcView.Lib.LibTheme import get_theme


class ViewButton(QWidget):
    """
    Add, remove, modify, search button
    """
    sig_add = OrcSignal()
    sig_delete = OrcSignal()
    sig_modify = OrcSignal()
    sig_search = OrcSignal()
    sig_select = OrcSignal()
    sig_cancel = OrcSignal()

    def __init__(self, p_style="HOR"):

        QWidget.__init__(self)

        # button is disabled by default
        self.__is_add = False
        self.__is_delete = False
        self.__is_modify = False
        self.__is_search = False
        self.__is_select = False
        self.__is_cancel = False

        # layout set
        if "HOR" == p_style:
            self.__layout = QHBoxLayout()
        else:
            self.__layout = QVBoxLayout()

        self.__layout.addStretch()
        self.setLayout(self.__layout)

    def enable_add(self):
        self.__is_add = True

    def enable_delete(self):
        self.__is_delete = True

    def enable_modify(self):
        self.__is_modify = True

    def enable_search(self):
        self.__is_search = True

    def enable_select(self):
        self.__is_select = True

    def enable_cancel(self):
        self.__is_cancel = True

    def create(self):
        """
        Create buttons and connect signal
        :return:
        """
        if self.__is_add:
            btn_add = QPushButton(u"增加")
            self.__layout.addWidget(btn_add)

            self.connect(btn_add, SIGNAL('clicked()'), self.sig_add.emit)

        if self.__is_delete:
            btn_delete = QPushButton(u"删除")
            self.__layout.addWidget(btn_delete)

            self.connect(btn_delete, SIGNAL('clicked()'), self.sig_delete.emit)

        if self.__is_modify:
            btn_modify = QPushButton(u"修改")
            btn_modify.setCheckable(True)
            self.__layout.addWidget(btn_modify)

            self.connect(btn_modify, SIGNAL('clicked()'), self.sig_modify.emit)

        if self.__is_search:
            btn_search = QPushButton(u"查询")
            self.__layout.addWidget(btn_search)

            self.connect(btn_search, SIGNAL('clicked()'), self.sig_search.emit)

        if self.__is_select:
            btn_select = QPushButton(u"选择")
            self.__layout.addWidget(btn_select)

            self.connect(btn_select, SIGNAL('clicked()'), self.sig_select.emit)

        if self.__is_cancel:
            btn_cancel = QPushButton(u"取消")
            self.__layout.addWidget(btn_cancel)

            self.connect(btn_cancel, SIGNAL('clicked()'), self.sig_cancel.emit)


class ViewButtons(QWidget):

    sig_clicked = OrcSignal(str)

    def __init__(self, p_def, p_direction="HOR"):
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

            self.__buttons["id"] = _button
            self.__layout.addWidget(_button)

        # 默认向右对齐
        self.align_back()

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
            self.__inputs[t_def['ID']] = create_editor(self, _def)

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
