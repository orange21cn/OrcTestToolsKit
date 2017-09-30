# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QStackedWidget
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from OrcLib.LibProgram import OrcFactory
from OrcView.Lib.LibBaseWidget import WidgetCreator


class DataBaseValueView(QWidget):

    clicked = OrcSignal()

    def __init__(self):

        QWidget.__init__(self)

        # 数据编辑器
        self._value_editor = WidgetCreator.create_text_area(self)

        # 数据源
        self._database_src = WidgetCreator.create_complex(self, 'DATASRC')

        layout = QVBoxLayout()
        layout.addWidget(self._database_src)
        layout.addWidget(self._value_editor)

        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        self._value_editor.clicked.connect(self.clicked.emit)
        self._database_src.clicked.connect(self.clicked.emit)

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        data = OrcFactory.create_default_dict(eval(p_data))

        self._database_src.set_data(data.value('SRC'))
        self._value_editor.set_data(data.value('SQL'))

    def get_data(self):
        """
        获取数据
        :return:
        """
        return str(dict(SRC=self._database_src.get_data(),
                        SQL=self._value_editor.get_data()))


class DataValueView(QStackedWidget):
    """
    用于数据的显示和编辑
    """
    clicked = OrcSignal()

    def __init__(self, parent=None):

        super(DataValueView, self).__init__(parent)

        # 默认编辑器
        self._default_editor = WidgetCreator.create_text_area(self)

        # sql 数据编辑器
        self._database_editor = DataBaseValueView()

        # 当前控件
        self._current_editor = self._default_editor

        self.addWidget(self._default_editor)
        self.addWidget(self._database_editor)

        self._default_editor.clicked.connect(self.clicked.emit)
        self._database_editor.clicked.connect(self.clicked.emit)

    def get_data(self):
        """
        获取数据
        :return:
        """
        return self._current_editor.get_data()

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        self._current_editor.set_data(p_data)

    def set_editor(self, p_index):
        """
        设置编辑器
        :param p_index:
        :param p_flag:
        :return:
        """
        if 2 == p_index:
            self.setCurrentIndex(1)
            self._current_editor = self._database_editor
        else:
            self.setCurrentIndex(0)
            self._current_editor = self._default_editor
