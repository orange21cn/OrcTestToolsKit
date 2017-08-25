# coding=utf-8
from PySide.QtCore import Qt
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QSplitter
from PySide.QtGui import QWidget

from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibBaseWidget import OrcBoxWidget

from .DataSrcListView import DataSrcListView
from .DataSrcDispView import DataSrcDispView
from .DataDebugView import DataDebugView


class DataSrcMain(QSplitter):
    """
    主界面
    """
    def __init__(self):

        QSplitter.__init__(self, Qt.Horizontal)

        self.title = u'数据源'

        # 数据源列表
        self.wid_src_list = DataSrcListView()

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

        layout_det = OrcBoxWidget('V')
        layout_det.add_widget(self.wid_src_det)
        layout_det.add_widget(self.buttons)

        layout_left = QSplitter(Qt.Vertical)
        layout_left.addWidget(self.wid_src_list)
        layout_left.addWidget(layout_det)

        self.addWidget(layout_left)
        self.addWidget(self.wid_sql_debug)
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(get_theme('Input'))

        self.editable(False)

        # 列表界面点击显示详细信息
        self.wid_src_list.sig_selected.connect(self.wid_src_det.set_data)

        # 点击后设置当前 DB
        self.wid_src_det.sig_db_changed.connect(self.wid_sql_debug.set_db)

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
            self.wid_src_list.model.mod_add(db_data)

        elif 'delete' == p_flag:

            self.wid_src_list.model.mod_delete()

        elif 'push' == p_flag:

            # 获取界面数据
            db_data = self.wid_src_det.get_data()

            # 更新
            self.wid_src_list.model.mod_update(db_data)

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
        self.wid_src_list.editable(p_flag)
        self.wid_src_det.set_editable(p_flag)

        if p_flag:
            for _id in 'add', 'push', 'delete':
                self.buttons.set_enable(_id)
        else:
            for _id in 'add', 'push', 'delete':
                self.buttons.set_disable(_id)
