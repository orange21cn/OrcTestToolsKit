# coding=utf-8
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTheme import get_theme

from .DataSrcListView import DataSrcListView
from .DataSrcDispView import DataSrcDispView
from .DataDebugView import DataDebugView


class DataSrcMain(QWidget):
    """
    主界面
    """
    def __init__(self):

        QWidget.__init__(self)

        self.title = u'数据源'

        # 数据源列表
        self.wid_src_lis = DataSrcListView()

        # 数据源详细信息
        self.wid_src_det = DataSrcDispView()

        # sql 调试界面
        self.wid_sql_debug = DataDebugView()

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

        # 点击后设置当前 DB
        self.wid_src_lis.sig_selected.connect(self.wid_sql_debug.set_db)

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
