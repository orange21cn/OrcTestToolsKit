# coding=utf-8
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibView import OrcTextArea

from DataResDispView import DataResDispView


class DataDebugView(QWidget):
    """
    SQL 编辑与调试窗口
    """
    def __init__(self):

        QWidget.__init__(self)

        # SQL 编辑窗口
        self.sql_editor = OrcTextArea()

        # SQL 结果显示
        self.res_disp = DataResDispView()

        # 按钮
        self.buttons = OrcButtons([
            dict(id="search", name=u"增加")
        ])

        layout_main = QVBoxLayout()
        layout_main.addWidget(self.sql_editor)
        layout_main.addWidget(self.res_disp)
        layout_main.addWidget(self.buttons)

        self.setLayout(layout_main)

        self.buttons.sig_clicked.connect(self.operate)

    def operate(self, p_flag):
        """
        点击按钮操作
        :param p_flag:
        :return:
        """
        if 'search' == p_flag:
            sql_text = self.sql_editor.get_data()
            self.res_disp.display.model.mod_search(dict(SQL=sql_text))

    def set_db(self, p_id):
        """
        设置数据库类型
        :param p_id:
        :return:
        """
        self.res_disp.display.model.service_set_db(p_id)
