# coding=utf-8
import abc

from PySide.QtCore import QAbstractTableModel
from PySide.QtCore import Qt
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QTableView

from OrcLib.LibCommon import is_null
from OrcLib.LibNet import get_config
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibLog import OrcLog
from OrcView.Lib.LibViewDef import ViewDefinition
from OrcView.Lib.LibViewDef import FieldDefinition
from OrcView.Lib.LibContextMenu import ViewContextMenu
from OrcView.Lib.LibView import get_dict
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibMain import LogClient


class ViewTable(QTableView):
    """
    View of table
    """
    sig_context = OrcSignal(str)

    def __init__(self):

        QTableView.__init__(self)

        self.__configer = get_config()
        self.__logger = LogClient()

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
                return self.__state_data[index.row()]["item_operate_text"]

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

    def usr_up(self):
        """
        上移
        :return:
        """
        if self.__state_current_data is None:
            return False

        step_id = self.__state_current_data["id"]
        self.__service.usr_up(step_id)

        self.usr_refresh()

        return True

    def usr_down(self):
        """
        下移
        :return:
        """
        if self.__state_current_data is None:
            return False

        step_id = self.__state_current_data["id"]
        self.__service.usr_down(step_id)

        self.usr_refresh()

        return True

    def usr_refresh(self):
        """
        Refresh the table when data changed
        :return:
        """
        if self.__state_cond is None:
            return

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
        for _field in p_def:

            if _field["DISPLAY"]:

                self.__state_fields_name.append(_field["NAME"])
                self.__state_fields_id.append(_field["ID"])

                if "SELECT" == _field["TYPE"]:
                    _res = get_dict(_field["ID"])
                    self.__state_select[_field["ID"]] = {}

                    for t_couple in _res:
                        self.__state_select[_field["ID"]][t_couple.dict_value] = t_couple.dict_text

                if _field["EDIT"]:
                    self.__state_edit_fields.append(_field["ID"])

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
        获取当前数据
        :return:
        """
        return self.__state_current_data


class ModelNewTableBase(QAbstractTableModel):
    """
    Base model
    """
    def __init__(self, p_flag):

        QAbstractTableModel.__init__(self)

        resource_dict = OrcResource("Dict")
        self.__logger = OrcLog("view.table.model")

        # 模型数据
        self._data = list()

        # 当前数据
        self._data_selected = None

        # 当前查询条件
        self._condition = dict()

        # 当前选择列表
        self._checked_list = list()

        # 界面字段定义
        self._definition = ViewDefinition(p_flag)

        # SELECT 类型的字段
        self.__state_select = dict()

        # 获取 SELECT 类型 value/text 数据对
        # {id: {value: text}, id: ....}
        for _field in self._definition.fields_display:

            assert isinstance(_field, FieldDefinition)

            if _field.display and "SELECT" == _field.type:

                _res = resource_dict.get(parameter=dict(dict_flag=_field.id))

                if not ResourceCheck.result_status(_res, u"获取字典值", self.__logger):
                    break

                self.__state_select[_field.id] = {item['dict_value']: item['dict_text'] for item in _res.data}

        # 当前可编辑状态
        self._state_editable = False

        # 记录数
        self._record_num = 0

    def headerData(self, section, orientation, role):
        """
        列名显示
        :param section:
        :param orientation:
        :param role:
        :return:
        """
        if role == Qt.DisplayRole:

            # 水平列显示列名
            if orientation == Qt.Horizontal:

                _field = self._definition.get_field_display_by_index(section)

                if _field is None:
                    return

                return _field.name

            # 垂直列显示索引
            else:
                return section

    def flags(self, index):
        """
        标识
        :param index:
        :return:
        """
        flag = super(ModelNewTableBase, self).flags(index)
        field = self._definition.get_field_display_by_index(index.column())

        if self._state_editable and field.edit:
            flag |= Qt.ItemIsEditable

        if index.column() == 0:
            flag |= Qt.ItemIsSelectable
            flag |= Qt.ItemIsUserCheckable

        return flag

    def rowCount(self, parent):
        """
        行数
        :param parent:
        :return:
        """
        return 0 if self._data is None else len(self._data)

    def columnCount(self, parent):
        """
        列数
        :param parent:
        :return:
        """
        return self._definition.display_length

    def data(self, index, role):
        """
        显示数据
        :param index:
        :param role:
        :return:
        """
        if (not index.isValid()) or (0 >= len(self._data)):
            return None

        if role == Qt.DisplayRole:

            _field = self._definition.get_field_display_by_index(index.column())
            assert isinstance(_field, FieldDefinition)

            _value = self._data[index.row()][_field.id]

            # Combobox 类型数据
            if "SELECT" == _field.type:
                try:
                    return self.__state_select[_field.id][_value]
                except KeyError:
                    self.__logger.error("select value error: %s, %s" % (_field.id, _value))

            # OPERATE 类型数据
            elif "OPERATE" == _field.type:
                return self._data[index.row()]["%s_text" % _field.id]

            # DISPLAY 类型数据
            elif "DISPLAY" == _field.type:
                return self._data[index.row()]["%s_text" % _field.id]

            # 其他类型数据,直接返回
            else:
                return _value

        if 0 == index.column() and role == Qt.CheckStateRole:

            if index.row() in self._checked_list:
                return Qt.Checked
            else:
                return Qt.Unchecked

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def setData(self, index, value, role=Qt.EditRole):
        """
        设置数据
        :param index:
        :param value:
        :param role:
        :return:
        """
        if role == Qt.EditRole:

            _cond = dict()
            _id = self._definition.fields_display[index.column()].id

            _cond["id"] = self._data[index.row()]["id"]
            _cond[_id] = value

            self.service_update(_cond)
            self._data[index.row()][_id] = value

            return value

        if role == Qt.CheckStateRole and index.column() == 0:

            if value:
                self._checked_list.append(index.row())
            else:
                self._checked_list.remove(index.row())

            return True


class ModelNewTable(ModelNewTableBase):

    def __init__(self, p_flg):

        ModelNewTableBase.__init__(self, p_flg)

    def mod_editable(self):
        """
        设置可编辑状态
        :return:
        """
        self._state_editable = not self._state_editable

    def mod_search(self, p_cond=None):
        """
        查询
        :param p_cond:
        :return:
        """
        self._condition = p_cond
        self.mod_refresh()

    def mod_add(self, p_data):
        """
        Add data
        :param p_data: {"id": ""value", ...}
        :return:
        """
        self._condition = self.service_add(p_data)
        self.mod_refresh()

    def mod_delete(self):
        """
        Delete all checked item
        :return:
        """
        # 获取列表
        del_list = list(self._data[_index]["id"] for _index in self._checked_list)

        # 删除
        self.service_delete(del_list)

        # 清空选取列表
        self._checked_list = []

        # 重置界面
        self.mod_refresh()

    def mod_up(self):
        """
        上移
        :return:
        """
        if self._data_selected is None:
            return False

        step_id = self._data_selected["id"]
        self.service_up(step_id)

        self.mod_refresh()

        return True

    def mod_down(self):
        """
        下移
        :return:
        """
        if self._data_selected is None:
            return False

        step_id = self._data_selected["id"]
        self.service_down(step_id)

        self.mod_refresh()

        return True

    def mod_refresh(self):
        """
        Refresh the table when data changed
        :return:
        """
        if self._condition is None:
            return

        # Clean condition
        for _key, value in self._condition.items():
            if is_null(value):
                self._condition.pop(_key)

        # Search
        data = self.service_search(self._condition)

        # 兼容分页与不分页
        if isinstance(data, dict):
            self._record_num = data["number"]
            self._data = data["data"]
        else:
            self._data = data

        # Clean checked list
        self._checked_list = []

        self.reset()

    def mod_clean(self):
        """
        Clean table
        :return:
        """
        self._data = []
        self._checked_list = []
        self.reset()

    def mod_get_data(self, p_row):
        """
        获取一行数据
        :param p_row:
        :return:
        """
        return self._data[p_row]

    def mod_set_current_data(self, p_index):
        """
        设置当前数据
        :param p_index:
        :return:
        """
        self._data_selected = self.mod_get_data(p_index.row())

    def mod_set_record_num(self, p_num):
        """
        设置记录数
        :param p_num:
        :return:
        """
        self._record_num = p_num

    def mod_get_record_num(self):
        """
        获取记录数
        :return:
        """
        return self._record_num

    def usr_get_current_data(self):
        """
        获取当前数据
        :return:
        """
        return self._data_selected

    @abc.abstractmethod
    def service_add(self, p_data):
        """
        调后台服务新增
        :param p_data:
        :return:
        """
        pass

    @abc.abstractmethod
    def service_delete(self, p_list):
        """
        调后台服务删除
        :param p_list:
        :return:
        """
        pass

    @abc.abstractmethod
    def service_update(self, p_data):
        """
        调后台服务更新
        :param p_data:
        :return:
        """
        pass

    @abc.abstractmethod
    def service_search(self, p_cond):
        """
        调后台服务查询
        :param p_cond:
        :return:
        """
        pass

    def service_up(self, p_id):
        """
        上移
        :param p_id:
        :return:
        """
        pass

    def service_down(self, p_id):
        """
        下移
        :param p_id:
        :return:
        """
        pass


class ViewNewTable(QTableView):
    """
    View of table
    """
    sig_context = OrcSignal(str)

    def __init__(self, p_flag, p_model, p_control):

        QTableView.__init__(self)

        self._configer = get_config()
        self._logger = LogClient()

        self._flag = p_flag

        # Model
        self.model = p_model()
        self.setModel(self.model)

        # Control
        self.control = p_control()
        self.setItemDelegate(self.control)

        # ---- Connection ----
        self.clicked.connect(self.model.mod_set_current_data)

        # 拉申最后一列
        self.horizontalHeader().setStretchLastSection(True)

        # 自适应列宽,貌似不起作用
        self.resizeColumnToContents(True)

        # 不显示格间距
        self.setShowGrid(False)

        # 设置样式
        self.setStyleSheet(get_theme("TableView"))

    def create_context_menu(self, p_menu_def):
        """
        右键菜单
        :param p_menu_def:
        :return:
        """
        _context_menu = ViewContextMenu(p_menu_def)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # connection
        self.customContextMenuRequested.connect(_context_menu.show_menu)
        _context_menu.sig_clicked.connect(self.sig_context.emit)
