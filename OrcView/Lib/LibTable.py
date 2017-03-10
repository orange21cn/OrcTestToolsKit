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
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibMain import LogClient


class ModelTableBase(QAbstractTableModel):
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

        # 当前可编辑状态
        self._state_editable = False

        # 可选择状态 todo
        self.__state_checkable = True

        # SELECT 类型的字段
        self.__definition_select = dict()

        # 获取 SELECT 类型 value/text 数据对
        # {id: {value: text}, id: ....}
        for _field in self._definition.fields_display:

            assert isinstance(_field, FieldDefinition)

            if _field.display and "SELECT" == _field.type:

                _res = resource_dict.get(parameter=dict(dict_flag=_field.id))

                if not ResourceCheck.result_status(_res, u"获取字典值", self.__logger):
                    break

                self.__definition_select[_field.id] = {item['dict_value']: item['dict_text'] for item in _res.data}

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
                    return None

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
        flag = super(ModelTableBase, self).flags(index)
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
                    return self.__definition_select[_field.id][_value]
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

        elif role == Qt.CheckStateRole:

            if 0 == index.column():

                if index.row() in self._checked_list:
                    return Qt.Checked
                else:
                    return Qt.Unchecked

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        else:
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


class ModelTable(ModelTableBase):

    def __init__(self, p_flg):

        ModelTableBase.__init__(self, p_flg)

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

    def mod_get_current_data(self):
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


class ViewTable(QTableView):
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
        # 设置当前数据
        self.clicked.connect(self.model.mod_set_current_data)

        # ---- Style ----
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
