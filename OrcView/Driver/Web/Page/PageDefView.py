# coding=utf-8
from PySide.QtGui import QDialog
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibAdd import BaseAdder
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibViewDef import view_page_def
from OrcView.Lib.LibMessage import OrcMessage

from .PageDefModel import PageDefModel
from .PageDefModel import PageDefControl


class PageDefView(OrcDisplayView):

    # 执行操作后发消息,以便更新页面信息及 debug 界面
    sig_action = OrcSignal(str)

    def __init__(self):

        OrcDisplayView.__init__(self)

        self.title = u"用例管理"

        # 控件定义
        self._def = WidgetDefinition('PageDef')
        self.main.definition.widget_def = self._def

        # 主控件
        self.model = PageDefModel(self._def)
        self.control = PageDefControl(self._def)
        self.view = ViewTable(self.model, self.control)
        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_add", name=u"增加"),
            dict(id="act_delete", name=u"删除"),
            dict(id="act_update", name=u"修改", type="CHECK"),
            dict(id="act_search", name=u"查询")]

        # Layout
        self.main.setContentsMargins(0, 0, 0, 0)

        # 初始化界面
        self.main.init_view()

        # +---- Connection ----+
        self.view.clicked.connect(self.act_select)

    def act_add(self):
        """
        新增
        :return:
        """
        _data = PageDefAdder.static_get_data()
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
        点击选择一条数据
        :return:
        """
        self.sig_action.emit('act_select')


class PageDefAdder(BaseAdder):
    """
    新增计划控件
    """
    def __init__(self):

        BaseAdder.__init__(self, 'PageDef')

        self.setWindowTitle(u'新增页面')

    @staticmethod
    def static_get_data():

        view = PageDefAdder()
        view.exec_()

        return view._data
