# coding=utf-8
from PySide.QtCore import QAbstractItemModel
from PySide.QtCore import QModelIndex
from PySide.QtCore import QMimeData
from PySide.QtCore import Qt

from cPickle import dumps, load
from cStringIO import StringIO

from OrcFrame.OrcCase.OrcCaseDef.CaseDefData import OrcCaseDef
from OrcFrame.OrcLib.LibView import BaseMagView


class PyMimeData(QMimeData):
    """
    The PyMimeData wraps a Python instance as MIME data.
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
            except:
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

        self.set_parent(p_parent)

    def set_parent(self, parent):
        if parent is not None:
            self.parent = parent
            self.parent.append_child(self)
        else:
            self.parent = None

    def append_child(self, child):

        self.children.append(child)

    def child_at_row(self, row):
        return self.children[row]

    def row_of_child(self, child):
        for i, item in enumerate(self.children):
            if item == child:
                return i
        return -1

    def remove_child(self, row):

        value = self.children[row]
        self.children.remove(value)

        return True

    def __len__(self):
        return len(self.children)


class LibTreeModel(QAbstractItemModel):
    """
    Model
    """
    def __init__(self):

        QAbstractItemModel.__init__(self)

        self.__table = OrcCaseDef()

        self.__ids = []
        self.__data = []

        self.__editable_columns = [0, 1, 2, 3]
        self.__editable_opened = False
        self.__cond = ""

        self.headers = self.__table.tab_get_field_names()[2:]
        self.__fields = self.__table.tab_get_field_ids()
        self.columns = len(self.headers) - 2

        self.__cond = ""
        self.__chk = []

        # Create items
        self.root = TreeNode([], None)
        self.__now_index = QModelIndex()

    def supportedDropActions(self):
        return Qt.CopyAction | Qt.MoveAction

    def flags(self, index):

        i_flag = QAbstractItemModel.flags(self, index)

        if index.isValid():
            i_flag |= Qt.ItemIsEditable
            i_flag |= Qt.ItemIsDragEnabled
            i_flag |= Qt.ItemIsDropEnabled
            i_flag |= Qt.ItemIsEnabled
            i_flag |= Qt.ItemIsSelectable
        else:
            i_flag |= Qt.ItemIsDropEnabled

        if index.column() == 0:
            i_flag |= Qt.ItemIsUserCheckable

        return i_flag

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

    def mimeTypes(self):
        types = ['application/x-ets-qt4-instance']
        return types

    def mimeData(self, index):
        node = self.usr_get_node(index[0])
        mine_data = PyMimeData(node)
        return mine_data

    def dropMimeData(self, p_mime_data, action, row, column, p_parent_index):

        if action == Qt.IgnoreAction:
            return True

        i_drag_node = p_mime_data.instance()
        i_parent_node = self.usr_get_node(p_parent_index)

        if 0 == len(i_parent_node.content):
            i_pid = "NULL"
        else:
            i_pid = i_parent_node.content[0]
        i_id = i_drag_node.content[0]

        self.__table.bas_modify("pid", i_pid, i_id)

        self.usr_refresh()

        return True

    def insertRow(self, row, parent):
        print "insertRow"
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        print "insertRows"
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, p_parent_index):
        print "removeRow"
        return self.removeRows(row, 1, p_parent_index)

    def index(self, row, column, parent):
        node = self.usr_get_node(parent)
        return self.createIndex(row, column, node.child_at_row(row))

    def data(self, index, role):

        item = index.internalPointer()

        if role == Qt.CheckStateRole:  # 被选中项是checkbox

            if index.column() == 0:
                for x in self.__chk:  # 检查该项是否在checkList中，如果在将其设为选中状态
                    if x == index:
                        return Qt.Checked
                else:
                    return Qt.Unchecked

        if role != Qt.DisplayRole:
            return None

        return item.content[index.column() + 2]

    def setData(self, index, value, role=Qt.EditRole):

        if role == Qt.CheckStateRole and 0 == index.column():

            if value == Qt.Unchecked:
                self.__chk.remove(index)
            else:
                self.__chk.append(index)

        return True

    def columnCount(self, parent):
        return self.columns

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

        assert row != - 1
        return self.createIndex(row, 0, parent)

    def usr_get_node(self, p_index):
        return p_index.internalPointer() if p_index.isValid() else self.root

    def usr_add(self, p_values, p_fields):

        if QModelIndex() == self.__now_index:
            i_pid = "NULL"
        else:
            i_pid = self.usr_get_node(self.__now_index).content[0]
        i_values = (str(i_pid), "10") + p_values

        self.__table.tab_add(i_values)
        self.usr_refresh()

    def usr_del(self):
        for t_index in self.__chk:
            t_id = self.usr_get_node(t_index).content[0]
            self.__table.bas_remove(t_id)
            self.__chk.remove(t_index)
            if self.__now_index == t_index:
                self.__now_index = QModelIndex()
            self.usr_refresh()

    def usr_editable(self):
        pass

    def usr_search(self, p_cond):

        # Get condition
        self.__cond = p_cond

        # Refresh
        self.usr_refresh()

    def usr_refresh(self):

        i_root = []

        self.usr_remove_children(self.root)

        # Search
        i_res = self.__table.tab_select("*", self.__cond)

        # Get root
        for item in i_res:
            t_root = self.__table.usr_get_root(item[0])

            if t_root not in i_root:
                i_root.append(t_root)
                t_temp = TreeNode(t_root, self.root)

        # Get tree
        for t_child in self.root.children:
            self.usr_append_subs(t_child)

        # Refresh
        t_data = self.__table.tab_select("*", self.__cond)

        self.__data = list(list(member)[1:] for member in t_data)
        self.__ids = list(list(member)[0] for member in t_data)

        self.reset()

    def usr_append_subs(self, p_node):

        i_items = self.__table.usr_get_children(p_node.content[0])

        if i_items is not None:

            for t_item in i_items:
                t_node = TreeNode(t_item, p_node)
                self.usr_append_subs(t_node)

    def usr_remove_children(self, p_node):

        while 0 != len(p_node.children):

            for t_node in p_node.children:
                if 0 == len(t_node.children):
                    p_node.children.remove(t_node)
                else:
                    self.usr_remove_children(t_node)

    def usr_set_index(self, p_index):
        self.__now_index = p_index


class CaseDefView(BaseMagView):

    def __init__(self):

        BaseMagView.__init__(self)

        table = OrcCaseDef()
        def_list = table.tab_get_def()
        list_search = def_list[2:6]
        list_new = def_list[3:7]

        self.__main_model = LibTreeModel()
        # main_control = CaseDefControl()

        self.create_view(list_search, list_new, "TREE")
        self.set_model(self.__main_model)
        # self.set_control(main_control)

        # Connection
        self.sig_search.connect(self.search)
        self.sig_del.connect(self.__main_model.usr_del)
        self.sig_modify.connect(self.__main_model.usr_editable)
        self.sig_add_submit[tuple, tuple].connect(self.add)

        self.sig_selected.connect(self.__main_model.usr_set_index)

    def get_line_data(self, p_line_no):
        return self.__main_model.get_data()[:][p_line_no]

    def search(self):
        self.__main_model.usr_search(self.widget_search.get_cond())

    def add(self, p_fields, p_values):
        self.__main_model.usr_add(p_values, p_fields)
        self.window_add.close()
