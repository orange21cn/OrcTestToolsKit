# coding=utf-8
import json

from PySide.QtCore import QAbstractTableModel
from PySide.QtCore import Qt
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QTableView

from OrcLib.LibCommon import is_null
from OrcLib.LibNet import get_config
from OrcView.Lib.LibContextMenu import ViewContextMenu
from OrcView.Lib.LibView import get_dict
from OrcView.Lib.LibView import operate_to_str
from OrcView.Lib.LibTheme import get_theme


class ViewTable(QTableView):
    """
    View of table
    """
    sig_context = OrcSignal(str)

    def __init__(self):

        QTableView.__init__(self)

        self.__configer = get_config()

        # 拉申最后一列
        self.horizontalHeader().setStretchLastSection(True)

        # ...
        self.resizeColumnToContents(True)

        # 不显示格间距
        self.setShowGrid(False)

        self.alternatingRowColors()

        self.setStyleSheet(get_theme("TableView"))

    def create_context_menu(self, p_def):
        """
        右键菜单
        :param p_def:
        :return:
        """
        _context_menu = ViewContextMenu(p_def)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # connection
        self.customContextMenuRequested.connect(_context_menu.show_menu)
        _context_menu.sig_clicked.connect(self.sig_context.emit)

    def set_model(self, p_model):
        """
        设置模型
        :param p_model:
        :return:
        """
        self.setModel(p_model)

    def set_control(self, p_control):
        """
        :param p_control:
        :return:
        """
        self.setItemDelegate(p_control)


class ModelTable(QAbstractTableModel):
    """
    Base model
    """
    def __init__(self):

        QAbstractTableModel.__init__(self)

        self.__state_current_data = None
        self.__state_cond = {}  # now sql condition
        self.__state_data = list()  # data
        self.__state_check = []  # checked list

        self.__state_fields_name = []  # fields CN name
        self.__state_fields_id = []  # data table field name
        self.__state_edit_fields = []
        self.__state_select = {}

        self._state_editable = False

        self.__record_num = 0

        self.__service = None

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.__state_fields_name[section]
            else:
                return section

    def flags(self, index):

        flag = super(ModelTable, self).flags(index)

        if self._state_editable and \
           (self.__state_fields_id[index.column()] in self.__state_edit_fields):
            flag |= Qt.ItemIsEditable

        if index.column() == 0:
            flag |= Qt.ItemIsSelectable
            flag |= Qt.ItemIsUserCheckable

        return flag

    def rowCount(self, parent):

        if self.__state_data is None:
            return 0
        else:
            return len(self.__state_data)

    def columnCount(self, parent):
        return len(self.__state_fields_name)

    def data(self, index, role):

        if not index.isValid():
            return None

        if role == Qt.DisplayRole:

            _id = self.__state_fields_id[index.column()]

            if 0 < len(self.__state_data):
                _value = self.__state_data[index.row()][_id]
            else:
                _value = None

            if _id in self.__state_select:
                try:
                    return self.__state_select[_id][_value]
                except KeyError:
                    pass

            elif "item_operate" == _id:
                return operate_to_str(json.loads(_value))

            else:
                return _value

        if 0 == index.column() and role == Qt.CheckStateRole:

            if index.row() in self.__state_check:
                return Qt.Checked
            else:
                return Qt.Unchecked

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def setData(self, index, value, role=Qt.EditRole):

        if role == Qt.EditRole:

            _cond = {}
            _field = self.__state_fields_id[index.column()]

            _cond["id"] = self.__state_data[index.row()]["id"]
            _cond[_field] = value

            self.__service.usr_update(_cond)
            self.__state_data[index.row()][_field] = value

            return value

        if role == Qt.CheckStateRole and index.column() == 0:

            if value:
                self.__state_check.append(index.row())
            else:
                self.__state_check.remove(index.row())

            return True

    def usr_editable(self):
        self._state_editable = not self._state_editable

    def usr_search(self, p_cond=None):
        self.__state_cond = p_cond
        self.usr_refresh()

    def usr_add(self, p_data):
        """
        Add data
        :param p_data: {"id": ""value", ...}
        :return:
        """
        self.__state_cond = self.__service.usr_add(p_data)
        self.usr_refresh()

    def usr_delete(self):
        """
        Delete all checked item
        :return:
        """
        # 获取列表
        _list = list(self.__state_data[_index]["id"] for _index in self.__state_check)

        # 删除
        self.__service.usr_delete(_list)

        # 清空选取列表
        self.__state_check = []

        # 重置界面
        self.usr_refresh()

    def usr_refresh(self):
        """
        Refresh the table when data changed
        :return:
        """
        # Clean condition
        for _key, value in self.__state_cond.items():
            if is_null(value):
                self.__state_cond.pop(_key)

        # Search
        data = self.__service.usr_search(self.__state_cond)

        # 分页有冲突
        if isinstance(data, dict):
            self.__record_num = data["number"]
            self.__state_data = data["data"]
        else:
            self.__state_data = data

        # Clean checked list
        self.__state_check = []

        self.reset()

    def usr_clean(self):
        """
        Clean table
        :return:
        """
        self.__state_data = []
        self.__state_check = []
        self.reset()

    def usr_set_service(self, p_service):
        """

        :param p_service:
        :return:
        """
        self.__service = p_service

    def usr_set_definition(self, p_def):
        """
        :param p_def:
        :return:
        """
        for t_field in p_def:

            if t_field["DISPLAY"]:

                self.__state_fields_name.append(t_field["NAME"])
                self.__state_fields_id.append(t_field["ID"])

                if "SELECT" == t_field["TYPE"]:
                    _res = get_dict(t_field["ID"])
                    self.__state_select[t_field["ID"]] = {}

                    for t_couple in _res:
                        self.__state_select[t_field["ID"]][t_couple.dict_value] = t_couple.dict_text

                if t_field["EDIT"]:
                    self.__state_edit_fields.append(t_field["ID"])

    def usr_get_data(self, p_row):
        """

        :param p_row:
        :return:
        """
        return self.__state_data[p_row]

    def usr_set_current_data(self, p_index):
        """

        :param p_index:
        :return:
        """
        self.__state_current_data = self.usr_get_data(p_index.row())

    def usr_set_record_num(self, p_num):
        """
        设置记录数
        :param p_num:
        :return:
        """
        self.__record_num = p_num

    def usr_get_record_num(self):
        """
        获取记录数
        :return:
        """
        return self.__record_num

    def usr_get_current_data(self):
        """

        :return:
        """
        return self.__state_current_data
