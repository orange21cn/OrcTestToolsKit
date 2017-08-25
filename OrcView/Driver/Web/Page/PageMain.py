# coding=utf-8
from OrcView.Driver.Web.Page.PageDetView import PageDetView
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QWidget

from OrcView.Driver.Web.Page.PageDefView import PageDefView
from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibViewDef import WidgetDefinition


class PageContainer(OrcDisplayView):
    """
    Page 总页面
    """
    sig_selected = OrcSignal(list)

    def __init__(self):

        OrcDisplayView.__init__(self)

        self.title = u"页面"

        self.main.definition.widget_def = WidgetDefinition('PageDef')

        # Search condition widget
        self.main.definition.search_enable = True
        self.main.definition.search_column = 2

        # Column widget
        self.view_page_def = PageDefView()
        self.view_page_det = PageDetView()
        self.main.display = QWidget()

        # Bottom layout
        layout_view = QHBoxLayout()
        layout_view.addWidget(self.view_page_def)
        layout_view.addWidget(self.view_page_det)
        self.main.display.setLayout(layout_view)

        # 初始化界面
        self.main.init_view()

        self.main.setContentsMargins(0, 0, 0, 0)
        layout_view.setContentsMargins(0, 0, 0, 0)
        layout_view.setSpacing(0)

        # +---- Connection ----+
        self.view_page_def.sig_action.connect(self._dispatch_action)
        self.view_page_det.sig_selected.connect(self.page_det_selected)

    def act_add(self):
        """
        新增时
        :return:
        """
        self.view_page_det.clean()

    def act_delete(self):
        """
        删除时
        :return:
        """
        self.view_page_det.clean()

    def act_search(self):
        """
        查询时
        :return:
        """
        condition = self.main.searcher.get_cond()
        self.view_page_def.model.mod_search(condition)
        self.view_page_det.clean()

    def act_select(self):
        """
        选择时
        :return:
        """
        page_def_data = self.view_page_def.model.mod_get_current_data()
        if not page_def_data:
            return

        self.view_page_det.set_page_id(page_def_data['id'])

    def page_det_selected(self):
        """
        发送数据给 debug
        :return:
        """
        self.sig_selected.emit(
            [self.view_page_def.model.mod_get_current_data(),
             self.view_page_det.model.mod_get_current_data()])
