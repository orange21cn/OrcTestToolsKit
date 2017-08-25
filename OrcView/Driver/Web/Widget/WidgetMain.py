# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QSplitter
from PySide.QtGui import QSizePolicy

from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Driver.Web.Widget.WidgetDetView import WidgetDetView
from OrcView.Driver.Web.Widget.WidgetDefView import WidgetDefView


class WidgetContainer(OrcDisplayView):

    sig_selected = OrcSignal(dict)

    def __init__(self):

        OrcDisplayView.__init__(self)

        self.title = u"控件"

        # 控件定义
        self._def = WidgetDefinition('WidgetDef')
        self.main.definition.widget_def = self._def

        # 查询条
        self.main.definition.search_enable = True
        self.main.definition.search_column = 2

        # 主控件
        self.view_widget_def = WidgetDefView()
        self.view_widget_det = WidgetDetView()
        self.view = QSplitter()

        self.view.addWidget(self.view_widget_def)
        self.view.addWidget(self.view_widget_det)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main.display = self.view

        # 初始化控件
        self.view.setContentsMargins(0, 0, 0, 0)
        self.main.setContentsMargins(0, 0, 0, 0)
        self.main.init_view()

        # +---- Connection ----+
        self.view_widget_def.sig_action.connect(self._dispatch_action)

    def act_add(self):
        """
        新增
        :return:
        """
        self.view_widget_det.model.mod_clean()

    def act_delete(self):
        """
        删除
        :return:
        """
        self.view_widget_det.model.mod_clean()

    def act_search(self):
        """
        查询
        :return:
        """
        self.view_widget_def.model.mod_search(self.main.searcher.get_cond())
        self.view_widget_det.model.mod_clean()

    def act_select(self):
        """
        选择
        :return:
        """
        widget_def_data = self.view_widget_def.model.mod_get_current_data()
        if not widget_def_data:
            return
        self.view_widget_det.set_widget(widget_def_data)
        self.sig_selected.emit(widget_def_data)
