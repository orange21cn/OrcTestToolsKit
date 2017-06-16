# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from PySide.QtGui import QSplitter
from PySide.QtGui import QTabWidget

from OrcLib.LibProgram import orc_singleton
from OrcView.Driver.Web.Page.PageMain import PageContainer
from OrcView.Driver.Web.Widget.WidgetMain import WidgetContainer
from OrcView.Driver.Web.Window.WindowView import WindowView
from OrcView.Lib.LibTheme import get_theme

from .Cmd.WebDebug import WebDebug


@orc_singleton
class ViewWebMain(QSplitter):
    """

    """
    sig_page_selected = OrcSignal(str)

    def __init__(self):

        QSplitter.__init__(self)

        self.title = u"Web对象管理"

        # Page
        _page = PageContainer()

        # Window
        _window = WindowView()

        # Widget
        _widget = WidgetContainer()

        # 页面 tab
        _tab = QTabWidget()
        _tab.addTab(_page, _page.title)
        _tab.addTab(_window, _window.title)
        _tab.addTab(_widget, _widget.title)

        _tab.setTabPosition(QTabWidget.West)
        _tab.setStyleSheet(get_theme("TabViewWeb"))

        # 测试区
        _debug = WebDebug()

        # 主layout
        self.addWidget(_tab)
        self.addWidget(_debug)

        self.setStretchFactor(0, 7)
        self.setStretchFactor(1, 3)

        self.setContentsMargins(0, 0, 0, 0)

        # 信号
        _tab.currentChanged.connect(_debug.set_index)
        _page.sig_selected.connect(_debug.set_data)
        _widget.sig_selected.connect(_debug.set_data)
