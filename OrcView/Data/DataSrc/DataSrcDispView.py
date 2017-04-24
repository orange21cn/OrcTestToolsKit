# coding=utf-8
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QStackedWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcLib import get_config
from OrcView.Lib.LibView import OrcSelect

from .DataSrc import DataSrcSqlite
from .DataSrc import DataSrcMySql
from .DataSrc import DataSrcOracle


class DataSrcDispView(QWidget):
    """
    数据源详细信息显示
    """
    def __init__(self):

        QWidget.__init__(self)

        self.__configer = get_config('data_src')

        self.wid_src_type = OrcSelect('data_src_type')
        self.wid_src_sqlite = DataSrcSqlite()
        self.wid_src_mysql = DataSrcMySql()
        self.wid_src_oracle = DataSrcOracle()

        self.wid_src_current = self.wid_src_sqlite

        self.wid_src = QStackedWidget()
        self.wid_src.addWidget(self.wid_src_sqlite)
        self.wid_src.addWidget(self.wid_src_mysql)
        self.wid_src.addWidget(self.wid_src_oracle)

        layout_type = QHBoxLayout()
        layout_type.addWidget(QLabel(u'数据库类型:'))
        layout_type.addWidget(self.wid_src_type)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_type)
        layout_main.addWidget(self.wid_src)

        self.setLayout(layout_main)

        self.wid_src_type.currentIndexChanged.connect(self.switch_data_src)

    def switch_data_src(self, p_index):
        """
        切换数据源界面
        :param p_index:
        :return:
        """
        self.wid_src.setCurrentIndex(p_index)

        if 0 == p_index:
            self.wid_src_current = self.wid_src_sqlite
        elif 1 == p_index:
            self.wid_src_current = self.wid_src_mysql
        elif 2 == p_index:
            self.wid_src_current = self.wid_src_oracle
        else:
            pass

    def set_data(self, p_id):
        """
        设置数据
        :param p_id:
        :return:
        """

        database_type = self.__configer.get_option(p_id, 'type')

        self.wid_src_type.set_data(database_type)
        self.wid_src_current.set_data(p_id)

    def get_data(self):
        """
        获取数据
        :return:
        """
        db_data = self.wid_src_current.get_data()
        db_data['type'] = self.wid_src_type.get_data()

        return db_data

    def editable(self, p_flag):
        """
        设置可编辑状态
        :param p_flag:
        :return:
        """
        self.wid_src_type.setEnabled(p_flag)
        self.wid_src_sqlite.editable(p_flag)
        self.wid_src_mysql.editable(p_flag)
        self.wid_src_oracle.editable(p_flag)
