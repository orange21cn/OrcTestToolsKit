# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QTabWidget
from PySide.QtGui import QVBoxLayout

from OrcView.Driver.Web.PageMain import PageContainer
from OrcView.Driver.Web.WidgetMain import WidgetContainer


class ViewWebMain(QWidget):
    """

    """
    def __init__(self):
        QWidget.__init__(self)

        # Page
        _page = PageContainer()

        # Window

        # Widget
        _widget = WidgetContainer()

        # 页面 tab
        _tab = QTabWidget()
        _tab.addTab(_page, "Page")
        _tab.addTab(_widget, "Widget")

        # 主layout
        _layout = QVBoxLayout()
        _layout.addWidget(_tab)

        self.setLayout(_layout)
