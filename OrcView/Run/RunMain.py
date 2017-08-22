# coding=utf-8
from PySide.QtGui import QSplitter
from PySide.QtGui import QTabWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget
from .Run.RunDetView import RunDetView

from OrcLib.LibProgram import orc_singleton
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibViewDef import view_run_def
from OrcView.Run.Report.ReportDet import ViewReportDet
from OrcView.Run.Run.RunDefView import RunDefView
from OrcView.Run.Debug.DebugMain import DebugMain


@orc_singleton
class RunMainView(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"执行"

        # 执行记录管理控件
        self.__wid_run_def = RunDefView()

        # 报告控件
        self.__wid_report_det = ViewReportDet()

        # 执行控件
        self.__wid_run_det = RunDetView()

        # 调试控件
        self.__wid_debug = DebugMain()

        # 查询控件
        self.__wid_search_cond = ViewSearch(view_run_def)

        # 显示控件 layout
        layout_right = QTabWidget()
        layout_right.addTab(self.__wid_debug, self.__wid_debug.title)
        layout_right.addTab(self.__wid_run_det, self.__wid_run_det.title)
        layout_right.addTab(self.__wid_report_det, self.__wid_report_det.title)

        layout_right.setTabPosition(QTabWidget.East)
        layout_right.setStyleSheet(get_theme("RunRes"))

        # 底部 layout
        layout_bottom = QSplitter()
        layout_bottom.addWidget(self.__wid_run_def)
        layout_bottom.addWidget(layout_right)

        # main layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.__wid_search_cond)
        layout_main.addWidget(layout_bottom)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        self._current_display = self.__wid_debug

        # 查询
        self.__wid_run_def.sig_search.connect(self.search)

        # 选择后更新右侧界面
        self.__wid_run_def.sig_selected.connect(self.refresh)

        # 更换 tab
        layout_right.currentChanged.connect(self.change_display)

        self.__wid_run_def.sig_start.connect(self.__wid_run_det.usr_start)

    def change_display(self, p_index):
        """
        切换当前控件
        :param p_index:
        :return:
        """
        if 0 == p_index:
            self._current_display = self.__wid_debug
        elif 1 == p_index:
            self._current_display = self.__wid_run_det
        else:
            self._current_display = self.__wid_report_det

    def refresh(self, p_path):
        """
        刷新显示界面
        :param p_path:
        :return:
        """
        self._current_display.usr_refresh(p_path)

    def search(self):
        """
        查询
        :return:
        """
        self.__wid_run_def.search(self.__wid_search_cond.get_cond())
