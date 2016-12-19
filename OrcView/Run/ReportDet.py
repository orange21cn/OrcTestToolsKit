# coding=utf-8
import os

from PySide.QtGui import QWidget
from PySide.QtWebKit import QWebView
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibSearch import ViewButtons
from ReportDetService import ReportDetService


class ViewReportDet(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.title = "报告"

        self.__path = None
        self.__service = ReportDetService()

        # report view
        self.__wid_display = QWebView()

        # buttons
        _wid_buttons = ViewButtons([
            dict(id="refresh", name=u'更新'),
            dict(id="export", name=u'导出')
        ])
        _wid_buttons.align_back()

        # main layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        _layout.setContentsMargins(0, 0, 0, 0)

        # connection

    def usr_refresh(self, p_path=None):

        if p_path is not None:
            self.__path = dict(path=p_path)

        report_path = self.__service.get_report_path(self.__path)
        self.__wid_display.setHtml(report_path)
