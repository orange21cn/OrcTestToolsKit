# coding=utf-8
from PySide.QtGui import QGridLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QWidget

from OrcLib import get_config

from OrcView.Lib.LibView import OrcLineEdit
from OrcView.Lib.LibView import OrcTextArea


class DataSrcSqlite(QWidget):
    """
    mysql 界面
    """
    def __init__(self):

        QWidget.__init__(self)

        self.__configer = get_config('data_src')

        self.inp_name = OrcLineEdit()
        self.inp_file = OrcLineEdit()
        self.inp_desc = OrcTextArea()

        layout_main = QGridLayout()
        layout_main.addWidget(QLabel(u'名称:'), 0, 0)
        layout_main.addWidget(self.inp_name, 0, 1)
        layout_main.addWidget(QLabel(u'文件:'), 1, 0)
        layout_main.addWidget(self.inp_file, 1, 1)
        layout_main.addWidget(QLabel(u'描述:'), 2, 0)
        layout_main.addWidget(self.inp_desc, 2, 1)

        self.setLayout(layout_main)

        self.editable(False)

    def set_data(self, p_id):
        """
        设置数据
        :param p_id:
        :return:
        """
        src_name = self.__configer.get_option(p_id, 'name')
        src_desc = self.__configer.get_option(p_id, 'desc')
        database_file = self.__configer.get_option(p_id, 'db_file')

        self.inp_name.set_data(src_name)
        self.inp_desc.set_data(src_desc)
        self.inp_file.set_data(database_file)

    def get_data(self):
        """
        获取数据
        :return:
        """
        return dict(
            name=self.inp_name.get_data(),
            desc=self.inp_desc.get_data(),
            db_file=self.inp_file.get_data()
        )

    def editable(self, p_flag):
        """
        设置可编辑状态
        :param p_flag:
        :return:
        """
        self.inp_name.setEnabled(p_flag)
        self.inp_file.setEnabled(p_flag)
        self.inp_desc.setEnabled(p_flag)


class DataSrcMySql(QWidget):
    """
    mysql 界面
    """
    def __init__(self):

        QWidget.__init__(self)

        self.__configer = get_config('data_src')

        self.inp_name = OrcLineEdit()
        self.inp_host = OrcLineEdit()
        self.inp_database = OrcLineEdit()
        self.inp_user = OrcLineEdit()
        self.inp_password = OrcLineEdit()
        self.inp_desc = OrcTextArea()

        layout_main = QGridLayout()
        layout_main.addWidget(QLabel(u'名称:'), 0, 0)
        layout_main.addWidget(self.inp_name, 0, 1)
        layout_main.addWidget(QLabel(u'主机2:'), 1, 0)
        layout_main.addWidget(self.inp_host, 1, 1)
        layout_main.addWidget(QLabel(u'数据库:'), 2, 0)
        layout_main.addWidget(self.inp_database, 2, 1)
        layout_main.addWidget(QLabel(u'用户名:'), 3, 0)
        layout_main.addWidget(self.inp_user, 3, 1)
        layout_main.addWidget(QLabel(u'密码:'), 0, 2)
        layout_main.addWidget(self.inp_password, 0, 3)
        layout_main.addWidget(QLabel(u'描述:'), 1, 2)
        layout_main.addWidget(self.inp_desc, 1, 3, 3, 1)

        self.setLayout(layout_main)

    def set_data(self, p_id):
        """
        设置数据
        :param p_id:
        :return:
        """
        name = self.__configer.get_option(p_id, 'name')
        desc = self.__configer.get_option(p_id, 'desc')
        database_host = self.__configer.get_option(p_id, 'db_host')
        database_name = self.__configer.get_option(p_id, 'db_name')
        database_user = self.__configer.get_option(p_id, 'db_user')
        database_passwd = self.__configer.get_option(p_id, 'db_passwd')

        self.inp_name.set_data(name)
        self.inp_desc.set_data(desc)
        self.inp_host.set_data(database_host)
        self.inp_database.set_data(database_name)
        self.inp_user.set_data(database_user)
        self.inp_password.set_data(database_passwd)

    def get_data(self):
        """
        获取数据
        :return:
        """
        return dict(
            name=self.inp_name.get_data(),
            desc=self.inp_desc.get_data(),
            db_host=self.inp_host.get_data(),
            db_name=self.inp_database.get_data(),
            db_user=self.inp_user.get_data(),
            db_passwd=self.inp_password.get_data()
        )

    def editable(self, p_flag):
        pass


class DataSrcOracle(QWidget):
    """
    mysql 界面
    """
    def __init__(self):

        QWidget.__init__(self)

        self.__configer = get_config('data_src')

        inp_host = OrcLineEdit()
        inp_str = OrcLineEdit()
        inp_user = OrcLineEdit()
        inp_password = OrcLineEdit()

        layout_main = QGridLayout()
        layout_main.addWidget(QLabel(u'主机3:'), 0, 0)
        layout_main.addWidget(inp_host, 0, 1)
        layout_main.addWidget(QLabel(u'数据库:'), 1, 0)
        layout_main.addWidget(inp_str, 1, 1)
        layout_main.addWidget(QLabel(u'用户名:'), 2, 0)
        layout_main.addWidget(inp_user, 2, 1)
        layout_main.addWidget(QLabel(u'密码:'), 3, 0)
        layout_main.addWidget(inp_password, 3, 1)

        self.setLayout(layout_main)

    def set_data(self, p_id):
        """
        设置数据
        :param p_id:
        :return:
        """
        pass

    def editable(self, p_flag):
        pass