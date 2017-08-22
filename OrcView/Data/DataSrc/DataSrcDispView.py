# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QFormLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QStackedWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcLib import get_config
from OrcLib.LibProgram import OrcFactory
from OrcView.Lib.LibBaseWidget import WidgetCreator

from .DataSrc import DataSrcEmpty
from .DataSrc import DataSrcSqlite
from .DataSrc import DataSrcMySql
from .DataSrc import DataSrcOracle

from DataSrcDispModel import DataSrcDispModel


class DataSrcDispView(QWidget):
    """
    数据源详细信息显示
    """
    sig_db_changed = OrcSignal(str)

    def __init__(self):

        QWidget.__init__(self)

        self.__configer = get_config('data_src')

        # 环境显示
        self.env = WidgetCreator.create_select('test_env', True)

        # 数据库类型
        self.wid_src_type = WidgetCreator.create_select('data_src_type', True)

        self._widget_lib = [
            DataSrcEmpty(),
            DataSrcSqlite(),
            DataSrcMySql(),
            DataSrcOracle()]

        # Model
        self._model = DataSrcDispModel()

        # 显示控件
        self.wid_src = QStackedWidget()
        for _wid in self._widget_lib:
            self.wid_src.addWidget(_wid)

        # 控件来源属性布局
        layout_env = QFormLayout()
        layout_env.addRow(u'环境:', self.env)
        layout_env.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        layout_type = QFormLayout()
        layout_type.addRow(u'数据库类型:', self.wid_src_type)
        layout_type.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        layout_property = QHBoxLayout()
        layout_property.addLayout(layout_env)
        layout_property.addLayout(layout_type)

        # 主布局
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_property)
        layout_main.addWidget(self.wid_src)

        self.setLayout(layout_main)

        # 数据源类型变化更新数据源信息
        self.wid_src_type.currentIndexChanged.connect(self.switch_data_src)

        # 测试环境变化
        self.env.currentIndexChanged.connect(self.set_data)

    def _current_widget(self):
        """
        当前数据库显示控件
        :return:
        """
        index = self.wid_src_type.currentIndex()
        return self._widget_lib[index]

    def switch_data_src(self, p_index):
        """
        切换数据源界面
        :param p_index:
        :return:
        """
        self.wid_src.setCurrentIndex(p_index)

        # 设置基本数据
        self._current_widget().set_data(self._model.mod_search())

    def set_data(self, p_info=None):
        """
        设置数据
        :param p_info:
        :return:
        """
        self.clean()

        result = self._model.mod_search(p_info, self.env.get_data())
        db_info = OrcFactory.create_default_dict(result)

        # 设置数据库类型
        self.wid_src_type.set_data(db_info.value('type', ''))

        # 设置数据库信息
        self._current_widget().set_data(db_info.dict())

        self.sig_db_changed.emit(self._model.mod_get_db_id())

    def get_data(self):
        """
        获取数据
        :return:
        """
        db_data = self._current_widget().get_data()
        db_data['type'] = self.wid_src_type.get_data()
        db_data['env'] = self.env.get_data()

        return db_data

    def clean(self):
        """
        清空
        :return:
        """
        for _widget in self._widget_lib:
            _widget.clean()

    def set_editable(self, p_flag):
        """
        设置可编辑状态
        :param p_flag:
        :return:
        """
        self.wid_src_type.setEnabled(p_flag)
        for _widget in self._widget_lib:
            _widget.set_enable(p_flag)
