# coding=utf-8
from PySide.QtGui import QDialog
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibAdd import BaseAdder
from OrcView.Lib.LibViewDef import view_widget_def
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibViewDef import WidgetDefinition

from .WidgetDefModel import WidgetDefModel
from .WidgetDefModel import WidgetDefControl


class WidgetDefView(OrcDisplayView):
    """
    控件信息
    """
    sig_action = OrcSignal(str)

    def __init__(self):

        OrcDisplayView.__init__(self)

        # 查询
        self._def = WidgetDefinition('WidgetDef')

        # 主控件
        self.model = WidgetDefModel(self._def)
        self.control = WidgetDefControl(self._def)
        self.view = ViewTree(self.model, self.control)
        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_add", name=u'增加'),
            dict(id="act_delete", name=u"删除"),
            dict(id="act_update", name=u"修改", type="CHECK"),
            dict(id="act_search", name=u"查询")]

        # 初始化界面
        self.main.setContentsMargins(0, 0, 0, 0)
        self.main.init_view()

        # +---- Connection ----+
        # 点击发送页面选择消息
        self.view.clicked.connect(self.act_select)

    def act_add(self):
        """
        新增
        :return:
        """
        _data = WidgetDefAdder.static_get_data()
        if _data is not None:
            self.model.mod_add(_data)
        self.sig_action.emit('act_add')

    def act_delete(self):
        """
        删除
        :return:
        """
        if OrcMessage.question(self, u"确认删除"):
            self.model.mod_delete()
            self.sig_action.emit('act_delete')

    def act_update(self):
        """
        修改
        :return:
        """
        self.model.basic_editable()

    def act_search(self):
        """
        查询
        :return:
        """
        self.sig_action.emit('act_search')

    def act_select(self):
        """
        发送点击信号
        :param p_index:
        :return:
        """
        self.sig_action.emit('act_select')


class WidgetDefAdder(BaseAdder):
    """
    新增计划控件
    """
    def __init__(self):

        BaseAdder.__init__(self, 'WidgetDef')

        self.setWindowTitle(u'新增控件')

    @staticmethod
    def static_get_data():

        view = WidgetDefAdder()
        view.exec_()

        return view._data


class WidgetDefSelector(QDialog):
    """

    """
    def __init__(self):

        QDialog.__init__(self)

        # Search
        self.__wid_search_cond = ViewSearch(view_widget_def, 2)

        # Data result display widget
        self.display = ViewTree(WidgetDefModel, WidgetDefControl)

        # Buttons window
        wid_buttons = OrcButtons([dict(id="search", name=u"查询")])

        # 禁止选择
        self.display.model.basic_checkable(False)

        # Layout
        layout_main = QVBoxLayout()

        layout_main.addWidget(self.__wid_search_cond)
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        self.setLayout(layout_main)

        # 点击按钮
        wid_buttons.sig_clicked.connect(self.operate)

        # 双击后关闭
        self.display.doubleClicked.connect(self.close)

    def operate(self, p_flg):
        """
        点击按钮操作
        :param p_flg:
        :return:
        """
        if "search" == p_flg:
            self.display.model.mod_search(self.__wid_search_cond.get_cond())
        else:
            pass

    @staticmethod
    def get_widget():
        """

        :return:
        """
        view = WidgetDefSelector()
        view.exec_()

        return view.display.model.mod_get_current_data()
