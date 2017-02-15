# coding=utf-8
from PySide.QtGui import QStyledItemDelegate
from PySide.QtCore import Qt
from OrcView.Lib.LibView import create_editor
from OrcView.Lib.LibViewDef import ViewDefinition
from OrcView.Lib.LibViewDef import FieldDefinition


class LibControl(QStyledItemDelegate):

    def __init__(self, p_def):

        QStyledItemDelegate.__init__(self)

        self._definition = []

        for _index in range(len(p_def)):

            if p_def[_index]["DISPLAY"]:
                self._definition.append(p_def[_index])

    def createEditor(self, parent, option, index):
        """
        生成编辑器
        :param parent:
        :param option:
        :param index:
        :return:
        """
        _def = dict(TYPE=self._definition[index.column()]["TYPE"],
                    SOURCE="EDITOR",
                    FLAG=self._definition[index.column()]["ID"])

        editor = create_editor(parent, _def)
        editor.set_data(index.data(Qt.DisplayRole))

        return editor

    def setEditorData(self, editor, index):
        """
        设置编辑器数据
        :param editor:
        :param index:
        :return:
        """
        item_str = index.data(Qt.DisplayRole)
        editor.set_data(item_str)

    def setModelData(self, editor, model, index):
        """
        设置模型数据
        :param editor:
        :param model:
        :param index:
        :return:
        """
        _data = editor.get_data()
        model.setData(index, _data)


class ControlNew(QStyledItemDelegate):

    def __init__(self, p_flag):

        QStyledItemDelegate.__init__(self)

        self._definition = ViewDefinition(p_flag)

    def createEditor(self, parent, option, index):
        """
        生成编辑器
        :param parent:
        :param option:
        :param index:
        :return:
        """
        field = self._definition.fields_display[index.column()]
        assert isinstance(field, FieldDefinition)

        _def = dict(TYPE=field.type,
                    SOURCE="EDITOR",
                    FLAG=field.id)

        editor = create_editor(parent, _def)
        editor.set_data(index.data(Qt.DisplayRole))

        return editor

    def setEditorData(self, editor, index):
        """
        设置编辑器数据
        :param editor:
        :param index:
        :return:
        """
        item_str = index.data(Qt.DisplayRole)
        editor.set_data(item_str)

    def setModelData(self, editor, model, index):
        """
        设置模型数据
        :param editor:
        :param model:
        :param index:
        :return:
        """
        _data = editor.get_data()
        model.setData(index, _data)