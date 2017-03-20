# coding=utf-8
import os
import sqlite3
import pymysql

from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QGridLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QStackedWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget
from sqlalchemy import exc

from OrcLib import get_config
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTable import StaticModelTable
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibView import OrcLineEdit
from OrcView.Lib.LibView import OrcSelect
from OrcView.Lib.LibView import OrcTextArea


class DataSrcControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'DataSrc')


class DataSrcModel(StaticModelTable):

    def __init__(self):

        StaticModelTable.__init__(self, 'DataSrc')

        self.__configer = get_config('data_src')

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        db_data = p_data

        # 获取 ID
        if 'id' in db_data:
            db_id = db_data['id']
            db_data.pop('id')
        else:
            ids = [int(item) for item in self.__configer.get_sections()]

            if ids:
                db_id = str(max(ids) + 1)
            else:
                db_id = '1'

            self.__configer.add_section(db_id)

        # 写入数据
        for _key, _value in db_data.items():
            self.__configer.set_option(db_id, _key, _value)

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        for _id in p_list:
            self.__configer.del_section(_id)

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :type p_data: dict
        :return:
        """
        db_data = p_data

        current_data = self.mod_get_current_data()
        if not current_data:
            return

        current_id = current_data['id']
        db_data["id"] = current_id

        cfg_data = self.__configer.get_options(current_id)
        for _key in cfg_data:
            self.__configer.del_option(current_id, _key)

        self.service_add(db_data)

    def service_search(self, p_data):
        """
        查询
        :param p_data:
        :return:
        """
        data_list = list()

        for _section in self.__configer.get_sections():

            # 文件为空时有缺陷,留一个 0 保证文件不为空
            # if '0' == _section:
            #     continue

            _name = self.__configer.get_option(_section, 'name')
            _desc = self.__configer.get_option(_section, 'desc')

            data_list.append(dict(
                id=_section,
                name=_name,
                desc=_desc
            ))

        return data_list


class DataSrcView(ViewTable):
    """
    显示
    """
    sig_selected = OrcSignal(str)

    def __init__(self):

        ViewTable.__init__(self, 'DataSrc', DataSrcModel, DataSrcControl)

        self.model.mod_search()

        self.clicked.connect(self.current_data)

    def current_data(self):
        """
        发送当前数据
        :return:
        """
        self.sig_selected.emit(self.model.mod_get_current_data()['id'])

    def editable(self, p_flag):
        """
        设置可编辑状态
        :param p_flag:
        :return:
        """
        self.model.mod_checkable(p_flag)
        self.model.reset()


class DataSrcDisp(QWidget):
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


class DataSrcMain(QWidget):
    """
    主界面
    """
    def __init__(self):

        QWidget.__init__(self)

        # 数据源列表
        self.wid_src_lis = DataSrcView()

        # 数据源详细信息
        self.wid_src_det = DataSrcDisp()

        # sql 调试界面
        self.wid_sql_debug = SqlDebug()

        # 按钮
        self.buttons = OrcButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="push", name=u"更新"),
            dict(id="connect", name=u"连接"),
        ])

        layout_left = QVBoxLayout()
        layout_left.addWidget(self.wid_src_lis)
        layout_left.addWidget(self.wid_src_det)
        layout_left.addWidget(self.buttons)

        layout_main = QHBoxLayout()
        layout_main.addLayout(layout_left)
        layout_main.addWidget(self.wid_sql_debug)

        self.setLayout(layout_main)

        self.setStyleSheet(get_theme('Input'))

        self.editable(False)

        # 列表界面点击显示详细信息
        self.wid_src_lis.sig_selected.connect(self.wid_src_det.set_data)

        # 点击按钮
        self.buttons.sig_clicked.connect(self.operate)

    def operate(self, p_flag):
        """
        按钮点击操作
        :param p_flag:
        :return:
        """
        if 'add' == p_flag:

            # 获取界面数据
            db_data = self.wid_src_det.get_data()

            # 增加
            self.wid_src_lis.model.mod_add(db_data)

        elif 'delete' == p_flag:

            self.wid_src_lis.model.mod_delete()

        elif 'push' == p_flag:

            # 获取界面数据
            db_data = self.wid_src_det.get_data()

            # 更新
            self.wid_src_lis.model.mod_update(db_data)

        elif 'update' == p_flag:

            status = self.buttons.get_status('update')

            self.editable(status)

        else:
            pass

    def editable(self, p_flag):
        """
        可编辑状态
        :param p_flag:
        :return:
        """
        self.wid_src_lis.editable(p_flag)
        self.wid_src_det.editable(p_flag)

        if p_flag:
            self.buttons.set_enable('add')
            self.buttons.set_enable('push')
            self.buttons.set_enable('delete')
        else:
            self.buttons.set_disable('add')
            self.buttons.set_disable('push')
            self.buttons.set_disable('delete')


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


class SqlDebug(QWidget):
    """
    SQL 编辑与调试窗口
    """
    def __init__(self):

        QWidget.__init__(self)

        sql_editor = OrcTextArea()
        res_disp = DataResDisp()

        layout_main = QVBoxLayout()
        layout_main.addWidget(sql_editor)
        layout_main.addWidget(res_disp)

        self.setLayout(layout_main)


class DataResDisp(QWidget):

    def __init__(self):

        QWidget.__init__(self)


class DBConnection(object):

    def __init__(self, p_type=None):

        pass

    def db_init(self):
        pass


class SQLiteConnection(object):

    def __init__(self, p_file):

        _file = p_file
        self._conn = None
        self._cursor = None

        if os.path.exists(_file):
            self._conn = sqlite3.connect(_file)
            self._cursor = self._conn.cursor()

    def db_execute(self, p_sql):
        """
        执行SQL
        :param p_sql:
        :return:
        """
        if self._cursor:
            self._cursor.execute(p_sql)
            return self._cursor.fetchall()
        else:
            return list()

    def db_test_connection(self):
        """
        测试连通性
        :return:
        """
        return self._conn is not None


class MySqlConnection(object):

    def __init__(self, p_host, p_port, p_user, p_passwd, p_db):

        try:
            self._conn = pymysql.connect(
                host=p_host,
                port=p_port,
                user=p_user,
                passwd=p_passwd,
                db=p_db,
                charset='utf8')

            self._cursor = self._conn.cursor()
        except exc.OperationalError:
            self._conn = None
            self._cursor = None

    def db_execute(self, p_sql):
        """
        执行SQL
        :param p_sql:
        :return:
        """
        if self._cursor:
            self._cursor.execute(p_sql)
            return self._cursor.fetchall()
        else:
            return list()

    def db_test_connection(self):
        """
        测试连通性
        :return:
        """
        return self._conn is None
