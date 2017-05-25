# coding=utf-8
import os

from PySide.QtGui import QWidget
from PySide.QtWebKit import QWebView
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QFileDialog
from PySide.QtGui import QPainter

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
        self.__wid_display.setRenderHint(QPainter.HighQualityAntialiasing)
        self.__wid_display.setRenderHint(QPainter.TextAntialiasing)

        # buttons
        wid_buttons = OrcButtons([
            dict(id="export", name=u'导出')
        ])
        wid_buttons.align_back()

        # main layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.__wid_display)
        layout_main.addWidget(wid_buttons)

        self.setLayout(layout_main)

        layout_main.setContentsMargins(0, 0, 0, 0)

        wid_buttons.sig_clicked.connect(self.operate)

    def operate(self, p_flag):
        """
        点击按钮操作
        :param p_flag:
        :return:
        """
        if 'export' == p_flag:

            result = QFileDialog.getSaveFileName(self, 'Save File', 'report.html', 'HTML Files(*.html *.htm)')
            report_file = result[0]

            with open(report_file, 'w') as rpt:
                content = self.__wid_display.page().currentFrame().toHtml()
                rpt.write(content.encode('utf-8'))

    def usr_refresh(self, p_path=None):
        """

        :param p_path:
        :return:
        """
        if p_path is not None:
            self.__path = dict(path=p_path)

        report_path = self.__service.get_report_path(self.__path)

        self.__wid_display.setUrl(report_path)
