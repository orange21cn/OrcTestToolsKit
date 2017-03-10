# coding=utf-8
import abc

from PySide.QtCore import Qt
from PySide.QtCore import QModelIndex
from PySide.QtCore import QAbstractItemModel
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibLog import OrcLog
from OrcLib import LibCommon
from OrcView.Lib.LibViewDef import ViewDefinition
from OrcView.Lib.LibViewDef import FieldDefinition


class OrcMimeData:
    pass


class TreeNode(object):
    """
    Tree data management
    """
    def __init__(self, p_content, p_parent=None):

        self.content = p_content
        self.parent = p_parent
        self.children = []

    def append_child(self, p_content):
        """
        Append child
        :param p_content:
        :return:
        """
        self.children.append(TreeNode(p_content, self))

    def append_node(self, p_node):
        """
        Append a child node
        :param p_node:
        :return:
        """
        p_node.parent = self
        self.children.append(p_node)

    def get_child(self, row):
        """
        Get the child
        :param row:
        :return:
        """
        return self.children[row]

    def get_index(self, child):
        """
        Get the index of child
        :param child:
        :return:
        """
        for _index, item in enumerate(self.children):
            if item == child:
                return _index

        return -1

    def remove_child(self, row):
        """
        Remove Child of row
        :param row:
        :return:
        """
        value = self.children[row]
        self.children.remove(value)

        return True

    def __len__(self):
        return len(self.children)


class ModelNewTreeBase(QAbstractItemModel):
    """
    Model
    """
    def __init__(self, p_flag):
        """
        :return:
        """
        QAbstractItemModel.__init__(self)

        resource_dict = OrcResource("Dict")

        self.__logger = OrcLog("view.tree.model")

        # 数据
        self._data = list()

        # 根节点
        self._root = TreeNode(None)

        # 当前数据
        self._data_selected = None

        # 查询条件
        self._condition = dict()

        # 当前选择列表
        self._checked_list = []

        # 可编辑状态
        self.__state_editable = False

        # 可选择状态
        self.__state_checkable = True

        # 界面字段定义
        self._definition = ViewDefinition(p_flag)

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

    def supportedDropActions(self):
        """
        支持拖拽
        :return:
        """
        return Qt.CopyAction | Qt.MoveAction

    def flags(self, index):
        """
        标识
        :param index:
        :return:
        """
        _flag = QAbstractItemModel.flags(self, index)

        if index.isValid():

            _field = self._definition.get_field_by_index(index.column())
            assert isinstance(_field, FieldDefinition)

            if self.__state_editable and _field.edit:
                _flag |= Qt.ItemIsEditable

            _flag |= Qt.ItemIsDragEnabled
            _flag |= Qt.ItemIsDropEnabled
            _flag |= Qt.ItemIsEnabled
            _flag |= Qt.ItemIsSelectable
        else:
            _flag |= Qt.ItemIsDropEnabled

        if index.column() == 0 and self.__state_checkable:
            _flag |= Qt.ItemIsUserCheckable

        return _flag

    def headerData(self, section, orientation, role):
        """
        列名显示
        :param section:
        :param orientation:
        :param role:
        :return:
        """
        # 显示
        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:

                _field = self._definition.get_field_display_by_index(section)

                if _field is None:
                    return None

                return _field.name

        # 对齐
        elif role == Qt.TextAlignmentRole:

            if orientation == Qt.Horizontal:
                return Qt.AlignHCenter

        return None

    def mimeTypes(self):
        """
        :return:
        """
        types = ['application/x-ets-qt4-instance']
        return types

    def mimeData(self, index):
        """
        :param index:
        :return:
        """
        node = self.node(index[0])
        mine_data = OrcMimeData(node)

        return mine_data

    def dropMimeData(self, mime_data, action, row, column, parent_index):
        """

        :param mime_data:
        :param action:
        :param row:
        :param column:
        :param parent_index:
        :return:
        """
        _cond = {}

        if action == Qt.IgnoreAction:
            return True

        drag_node = mime_data.instance()
        parent_node = self.node(parent_index)

        _cond['id'] = drag_node.content['id']
        if parent_node.content is None:
            _cond['pid'] = ""
        else:
            _cond['pid'] = parent_node.content['id']

        self.mod_update(_cond)

        self.mod_refresh()

        return True

    def index(self, row, column, parent):
        """

        :param row:
        :param column:
        :param parent:
        :return:
        """
        node = self.node(parent)
        return self.createIndex(row, column, node.get_child(row))

    def data(self, index, role):
        """

        :param index:
        :param role:
        :return:
        """
        item = index.internalPointer()

        # 显示数据
        if role == Qt.DisplayRole:

            _field = self._definition.get_field_display_by_index(index.column())
            assert isinstance(_field, FieldDefinition)

            _value = item.content[_field.id]

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

            if _field.id in self.__definition_select:
                return self.__definition_select[_field.id][_value]
            else:
                return _value

        # 字段选择状态
        elif role == Qt.CheckStateRole:

            if (index.column() == 0) and self.__state_checkable:

                if index in self._checked_list:
                    return Qt.Checked
                else:
                    return Qt.Unchecked

        # 对齐
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def setData(self, index, value, role=Qt.EditRole):
        """

        :param index:
        :param value:
        :param role:
        :return:
        """
        if role == Qt.EditRole:

            _cond = {}
            _field = self._definition.get_field_display_by_index(index.column())

            _cond["id"] = self.node(index).content["id"]
            _cond[_field.id] = value

            self.mod_update(_cond)
            self.node(index).content[_field.id] = value

            return value

        elif role == Qt.CheckStateRole:

            if 0 == index.column():

                if value == Qt.Unchecked:
                    self._checked_list.remove(index)
                else:
                    self._checked_list.append(index)

            return True

    def columnCount(self, parent):
        """

        :param parent:
        :return:
        """
        return self._definition.display_length

    def rowCount(self, parent):
        """

        :param parent:
        :return:
        """
        node = self.node(parent)
        if node is None:
            return 0
        return len(node)

    def parent(self, p_index):
        """

        :param p_index:
        :return:
        """
        if not p_index.isValid():
            return QModelIndex()

        node = self.node(p_index)
        if node is None:
            return QModelIndex()

        parent = node.parent
        if parent is None:
            return QModelIndex()

        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()

        row = grandparent.get_index(parent)

        return self.createIndex(row, 0, parent)

    def node(self, index):
        """
        获取节点
        :param index:
        :return:
        """
        if index.isValid():
            return index.internalPointer()
        else:
            return self._root


class ModelNewTree(ModelNewTreeBase):

    def __init__(self, p_def):

        ModelNewTreeBase.__init__(self, p_def)

    def mod_add(self, p_values):
        """
        新增
        :param p_values:
        :return:
        """
        values = p_values

        # 父元素只能有一个
        if 1 == len(self._checked_list):
            pid = self.node(self._checked_list[0]).content['id']

            # 设置父元素 id
            if pid is not None:
                values['pid'] = pid
        else:
            return None

        # 新增
        self._condition = self.service_add(values)

        # 刷新界面
        self.mod_refresh()

    def mod_delete(self):
        """
        删除
        :return:
        """
        del_list = [self.node(_index).content['id'] for _index in self._checked_list]
        self.service_delete(del_list)

        # 清空选取 list
        self._checked_list = list()

        # 重置界面
        self.mod_refresh()

    def mod_editable(self):
        """
        设置编辑状态
        :return:
        """
        self.__state_editable = not self.__state_editable

    def mod_checkable(self):
        """
        设置可选择
        :return:
        """
        self.__state_checkable = not self.__state_checkable

    def mod_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        # Get condition
        self._condition = dict() if p_cond is None else p_cond

        # Refresh
        self.mod_refresh()

    def mod_refresh(self):
        """
        刷新
        :return:
        """
        # Clean condition
        for _key, value in self._condition.items():
            if LibCommon.is_null(value):
                self._condition.pop(_key)

        # Remove node tree
        self._root.children = list()

        # Search
        result = self.service_search(self._condition)
        self._data = result

        if not isinstance(self._data, list):
            self._data = list()

        for _item in self._data:

            if ('None' == _item['pid']) or (_item['pid'] is None):
                self._root.append_node(self.mod_create_tree_node(_item))

        # Clean checked list
        self._checked_list = list()

        # 重置
        self.reset()

    def mod_set_data(self, p_para, p_list=None):
        """
        设置model数据,并重置界面
        :param p_list:
        :param p_para:
        :type p_para: dict
        :return:
        """
        if not isinstance(p_para, dict):
            import json
            parameter = json.loads(json.loads(p_para))
        else:
            parameter = p_para

        if "id" not in parameter:
            return

        if p_list is None:
            node = self._root
        else:
            node = p_list

        if (node.content is not None) and \
           (parameter["id"] == node.content["id"]):

            for name, value in parameter.items():

                if "id" == name:
                    continue

                if name in node.content:
                    node.content[name] = value

            self.reset()

        else:

            for _child in node.children:

                self.mod_set_data(parameter, _child)

    def mod_create_tree_node(self, p_cont):
        """
        Add all data to root node
        :param p_cont:
        :return:
        """
        _node = TreeNode(p_cont)

        for i in self._data:

            if p_cont['id'] == i['pid']:

                t_node = self.mod_create_tree_node(i)
                _node.append_node(t_node)

        return _node

    def mod_get_checked(self):
        """
        获取可选择列表
        :return:
        """
        _checked = []

        for t_index in self._checked_list:
            _checked.append(self.node(t_index).content["id"])

        return _checked

    def mod_get_editable(self):
        """
        获取可编辑属性
        :return:
        """
        return self.__state_editable

    def mod_set_current_data(self, p_index):
        """
        设置当前数据
        :param p_index:
        :return:
        """
        self._data_selected = self.node(p_index)

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
