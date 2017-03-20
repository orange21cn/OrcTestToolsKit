# coding=utf-8
import os

from PySide.QtGui import QWidget
from PySide.QtWebKit import QWebView
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibSearch import OrcButtons
from ReportDetService import ReportDetService


class ViewReportDet(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"报告"

        self.__path = None
        self.__service = ReportDetService()

        # report view
        self.__wid_display = QWebView()

        # buttons
        wid_buttons = OrcButtons([
            dict(id="refresh", name=u'更新'),
            dict(id="export", name=u'导出')
        ])
        wid_buttons.align_back()

        # main layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.__wid_display)
        layout_main.addWidget(wid_buttons)

        self.setLayout(layout_main)

        layout_main.setContentsMargins(0, 0, 0, 0)

    def usr_refresh(self, p_path=None):

        if p_path is not None:
            self.__path = dict(path=p_path)

        report_path = self.__service.get_report_path(self.__path)

        self.__wid_display.setUrl(report_path)
