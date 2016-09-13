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
from PySide.QtCore import QMargins

from OrcView.Lib.LibView import create_editor


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

    def __init__(self, p_def, p_direction="HORIZON"):
        """
        生成一个按钮组
        :param p_def: [{"id": t_id, "name": _name}]
        :return: None
        """
        QWidget.__init__(self)

        self.__definition = p_def  # 定义
        self.__direction = p_direction  # 方向

        # 设置方向
        if "HORIZON" == self.__direction:
            self.__layout = QHBoxLayout()
        else:
            self.__layout = QVBoxLayout()

        # 设置 layout
        self.setLayout(self.__layout)

        # 添加按钮
        for t_def in self.__definition:

            t_id = t_def["id"]
            t_name = t_def["name"]

            t_button = QPushButton(t_name)
            t_button.clicked.connect(partial(self.sig_clicked.emit, t_id))

            self.__layout.addWidget(t_button)

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

    def set_no_spacing(self):
        self.__layout.setSpacing(0)


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

        self.__fields_def = p_def

        self.__columns = 3
        self.__inputs = {}

        self.__layout_srh = QGridLayout()
        self.setLayout(self.__layout_srh)

    def set_col_num(self, p_num):
        self.__columns = p_num

    def create(self):

        _items = []

        for t_def in self.__fields_def:

            if not t_def['SEARCH']:
                continue

            t_label = QLabel(t_def['NAME'] + ":")
            _def = dict(TYPE=t_def["TYPE"],
                        SOURCE="SEARCH",
                        FLAG=t_def["ID"])
            self.__inputs[t_def['ID']] = create_editor(self, _def)

            t_layout = QHBoxLayout()
            t_layout.addWidget(t_label)
            t_layout.addWidget(self.__inputs[t_def['ID']])

            _items.append(t_layout)

        for t_index in range(len(_items)):
            t_row = t_index % self.__columns
            t_column = t_index / self.__columns

            self.__layout_srh.addLayout(_items[t_index], t_column, t_row)

    def get_cond(self):

        _cond = {}

        for t_inp in self.__inputs:
            t_value = self.__inputs[t_inp].get_data()
            _cond[t_inp] = t_value

        return _cond
