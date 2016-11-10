# coding=utf-8

from PySide.QtGui import QStyledItemDelegate
from PySide.QtCore import Qt
from OrcView.Lib.LibView import create_editor


class LibControl(QStyledItemDelegate):

    def __init__(self, p_def):

        QStyledItemDelegate.__init__(self)

        self._definition = []

        for t_index in range(len(p_def)):

            if p_def[t_index]["DISPLAY"]:
                self._definition.append(p_def[t_index])

    def createEditor(self, parent, option, index):

        _def = dict(TYPE=self._definition[index.column()]["TYPE"],
                    SOURCE="EDITOR",
                    FLAG=self._definition[index.column()]["ID"])
        t_editor = create_editor(parent, _def)
        t_editor.set_data(index.data(Qt.DisplayRole))

        return t_editor

    def setEditorData(self, editor, index):
        item_str = index.data(Qt.DisplayRole)
        editor.set_data(item_str)

    def setModelData(self, editor, model, index):
        _data = editor.get_data()
        model.setData(index, _data)

