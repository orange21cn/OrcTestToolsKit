# coding=utf-8
from cPickle import dumps
from cPickle import load
from cStringIO import StringIO

from PySide.QtCore import Qt
from PySide.QtCore import QMimeData
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal
from PySide.QtCore import QAbstractItemModel
from PySide.QtGui import QAbstractItemView
from PySide.QtGui import QTreeView

from OrcLib.LibCommon import is_null
# from OrcLib.LibNet import orc_invoke
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibContextMenu import ViewContextMenu
from OrcView.Lib.LibView import get_dict


class ViewTree(QTreeView):
    """
    Base tree view
    """
    sig_context = OrcSignal(str)

    def __init__(self):

        QTreeView.__init__(self)

        # MVC
        # 可拖拽
        self.dragEnabled()

        # 可释放
        self.acceptDrops()

        # 拖拽  indicator
        self.showDropIndicator()

        # 拖拽模式
        self.setDragDropMode(QAbstractItemView.InternalMove)

        # 标题拉伸最后一列
        self.header().setStretchLastSection(True)

        # 无 focus, 去掉蓝框
        self.setFocusPolicy(Qt.NoFocus)

        # 设置样式
        self.setStyleSheet(get_theme("TreeView"))

    def create_context_menu(self, p_def):
        """
        右键菜单
        :param p_def:
        :return:
        """
        context_menu = ViewContextMenu(p_def)

        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # 连接
        self.customContextMenuRequested.connect(context_menu.show_menu)
        context_menu.sig_clicked.connect(self.sig_context.emit)

    def set_model(self, p_model):
        """
        设置模型
        :param p_model:
        :return:
        """
        self.setModel(p_model)

    def set_control(self, p_control):
        """
        设置 Control
        :param p_control:
        :return:
        """
        self.setItemDelegate(p_control)


class OrcMimeData(QMimeData):
    """
    The OrcMimeData wraps a Python instance as MIME data.
    """
    MIME_TYPE = str('application/x-ets-qt4-instance')

    def __init__(self, p_data=None):
        """
        Initialise the instance.
        """
        QMimeData.__init__(self)

        # Keep a local reference to be returned if possible.
        self._local_instance = p_data

        if p_data is not None:
            # We may not be able to pickle the data.
            try:
                p_data = dumps(p_data)
            except Exception:
                return

            self.setData(self.MIME_TYPE, dumps(p_data.__class__) + p_data)

    def instance(self):
        """
        Return the instance.
        """
        if self._local_instance is not None:
            return self._local_instance

        io = StringIO(str(self.data(self.MIME_TYPE)))

        try:
            # Skip the type.
            load(io)

            # Recreate the instance.
            return load(io)
        except:
            pass

        return None


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


class ModelTree(QAbstractItemModel):
    """
    Model
    """
    def __init__(self):
        """
        :return:
        """
        QAbstractItemModel.__init__(self)

        self.__service = None

        self.__state_current_data = None
        self.__state_cond = {}  # now sql condition
        self._state_root = TreeNode(None)  # data root
        self.__state_list = []  # data list
        self.__state_check = []  # checked list

        self.__state_fields_name = []  # fields CN name
        self.__state_fields_id = []  # data table field name
        self.__state_edit_fields = []
        self.__state_select = {}

        self.__state_editable = False
        self.__state_chk_able = True

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def flags(self, index):

        _flag = QAbstractItemModel.flags(self, index)

        if index.isValid():
            if self.__state_editable and \
               self.__state_fields_id[index.column()] in self.__state_edit_fields:
                _flag |= Qt.ItemIsEditable
            _flag |= Qt.ItemIsDragEnabled
            _flag |= Qt.ItemIsDropEnabled
            _flag |= Qt.ItemIsEnabled
            _flag |= Qt.ItemIsSelectable
        else:
            _flag |= Qt.ItemIsDropEnabled

        if index.column() == 0 and self.__state_chk_able:
            _flag |= Qt.ItemIsUserCheckable

        return _flag

    def headerData(self, section, orientation, role):

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.__state_fields_name[section]

        if orientation == Qt.Horizontal and role == Qt.TextAlignmentRole:
            return Qt.AlignHCenter

        return None

    def mimeTypes(self):
        types = ['application/x-ets-qt4-instance']
        return types

    def mimeData(self, index):

        node = self.usr_get_node(index[0])
        mine_data = OrcMimeData(node)

        return mine_data

    def dropMimeData(self, p_mime_data, action, row, column, p_parent_index):

        _cond = {}

        if action == Qt.IgnoreAction:
            return True

        drag_node = p_mime_data.instance()
        parent_node = self.usr_get_node(p_parent_index)

        _cond['id'] = drag_node.content['id']
        if parent_node.content is None:
            _cond['pid'] = ""
        else:
            _cond['pid'] = parent_node.content['id']

        self.__service.usr_update(_cond)

        self.usr_refresh()

        return True

    def index(self, row, column, parent):
        node = self.usr_get_node(parent)
        return self.createIndex(row, column, node.get_child(row))

    def data(self, index, role):

        item = index.internalPointer()

        if role == Qt.CheckStateRole and \
           index.column() == 0 and \
           self.__state_chk_able:

            _state = Qt.Unchecked
            for x in self.__state_check:
                if x == index:
                    _state = Qt.Checked
                    break

            return _state

        if role == Qt.DisplayRole:

            _id = self.__state_fields_id[index.column()]
            _value = item.content[_id]

            if _id in self.__state_select:
                return self.__state_select[_id][_value]
            else:
                return _value

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def setData(self, index, value, role=Qt.EditRole):

        if role == Qt.EditRole:

            _cond = {}
            _field = self.__state_fields_id[index.column()]

            _cond["id"] = self.usr_get_node(index).content["id"]
            _cond[_field] = value

            self.__service.usr_update(_cond)
            self.usr_get_node(index).content[_field] = value

            return value

        if role == Qt.CheckStateRole and 0 == index.column():

            if value == Qt.Unchecked:
                self.__state_check.remove(index)
            else:
                self.__state_check.append(index)

            return True

    def columnCount(self, parent):
        return len(self.__state_fields_name)

    def rowCount(self, parent):
        node = self.usr_get_node(parent)
        if node is None:
            return 0
        return len(node)

    def parent(self, p_index):

        if not p_index.isValid():
            return QModelIndex()

        node = self.usr_get_node(p_index)

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

    def usr_set_service(self, p_service):
        self.__service = p_service

    def usr_set_definition(self, p_def):
        """
        Init definition
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

    def usr_get_node(self, p_index):
        return p_index.internalPointer() if p_index.isValid() else self._state_root

    def usr_add(self, p_values):
        """

        :param p_values:
        :return:
        """
        _pid = None
        _values = p_values

        if 1 == len(self.__state_check):
            _pid = self.usr_get_node(self.__state_check[0]).content['id']

        if _pid is not None:
            _values['pid'] = _pid

        self.__state_cond = self.__service.usr_add(_values)

        self.usr_refresh()

    def usr_delete(self):
        """

        :return:
        """
        del_list = [self.usr_get_node(_index).content['id'] for _index in self.__state_check]
        self.__service.usr_delete(del_list)

        # 清空选取 list
        while self.__state_check:
            self.__state_check.pop()

        # 重置界面
        self.usr_refresh()

    def usr_editable(self):

        self.__state_editable = not self.__state_editable

    def usr_chk_able(self):

        self.__state_chk_able = not self.__state_chk_able

    def usr_search(self, p_cond):

        # Get condition
        self.__state_cond = p_cond

        # Refresh
        self.usr_refresh()

    def usr_refresh(self):

        # Clean condition
        for _key, value in self.__state_cond.items():
            if is_null(value):
                self.__state_cond.pop(_key)

        # Remove node tree
        self.usr_remove_children(self._state_root)

        # Search
        self.__state_list = self.__service.usr_search(self.__state_cond)

        if self.__state_list is None:
            self.__state_list = []

        for t_item in self.__state_list:

            if 'None' == t_item['pid'] or t_item['pid'] is None:

                t_node = self.usr_create_tree_node(t_item)
                self._state_root.append_node(t_node)

        # Clean checked list
        for i in self.__state_check:
            self.__state_check.remove(i)

        self.reset()

    def usr_remove_children(self, p_node):

        while 0 != len(p_node.children):

            for t_node in p_node.children:
                if 0 == len(t_node.children):
                    p_node.children.remove(t_node)
                else:
                    self.usr_remove_children(t_node)

    def usr_set_data(self, p_para, p_list=None):
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
            node = self._state_root
        else:
            node = p_list

        if (node.content is not None) and \
           (parameter["id"] == node.content["id"]):

            for name, value in parameter.items():

                if "id" == name:
                    continue

                if name in node.content:
                    node.content[name] = value

            print node.content

            self.reset()

        else:

            for _child in node.children:

                self.usr_set_data(parameter, _child)

    def usr_create_tree_node(self, p_cont):
        """
        Add all data to root node
        :param p_cont:
        :return:
        """
        _node = TreeNode(p_cont)

        for i in self.__state_list:

            if p_cont['id'] == i['pid']:

                t_node = self.usr_create_tree_node(i)
                _node.append_node(t_node)

        return _node

    def usr_get_checked(self):

        _checked = []

        for t_index in self.__state_check:
            _checked.append(self.usr_get_node(t_index).content["id"])

        return _checked

    def usr_get_editable(self):
        return self.__state_editable

    def usr_set_current_data(self, p_index):
        self.__state_current_data = self.usr_get_node(p_index)

    def usr_get_current_data(self):
        return self.__state_current_data
