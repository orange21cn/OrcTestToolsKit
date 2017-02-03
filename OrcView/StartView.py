# coding=utf-8
import subprocess
from PySide.QtGui import QMainWindow
from PySide.QtGui import QTabWidget
from PySide.QtGui import QAction
from PySide.QtCore import SIGNAL
from PySide.QtCore import Qt

from OrcLib import get_config
from OrcLib.LibNet import OrcSocketResource
from OrcView.Lib.LibMain import DockCategory
from OrcView.Lib.LibMain import DockDetail
from OrcView.Lib.LibMain import DockLog
from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTheme import get_theme
from OrcView.Batch.BatchDef import ViewBatchDefMag
from OrcView.Batch.BatchDet import ViewBatchDetMag
from OrcView.Case.Case import ViewCaseDefMag
from OrcView.Case.StepMain import StepContainer
from OrcView.Data.DataDef import ViewDataMag
from OrcView.Driver.Web.WebMain import ViewWebMain
from OrcView.Run.RunMain import ViewRunMain
from OrcView.Run.ReportMain import ViewReportMain


class StartView(QMainWindow):

    def __init__(self):

        super(StartView, self).__init__()

        self.setWindowTitle("hello")
        self.resize(1024, 768)

        # 建立菜单栏
        self.create_menu()

        # 建立工具栏
        self.create_tools()

        # Dock
        self.dock_category = DockCategory()  # category widget
        # self.dock_log = DockBottom()  # log widget
        self.dock_detail = DockDetail()  # detail widget

        # center widget
        self.__wid_center = QTabWidget()
        self.setCentralWidget(self.__wid_center)

        self.__wid_center.setStyleSheet(get_theme("TabViewMain"))

        self.__wid_center.setTabsClosable(True)
        self.connect(self.__wid_center, SIGNAL("tabCloseRequested(int)"), self.close_tab)

    def create_menu(self):
        """
        建立菜单
        :return:
        """
        menu = self.menuBar()
        menu_def = (
            ('Create', (
                ('Batch', self.open_batch),
                ('Case', self.open_case),
                ('Data', self.open_data),
                ('Web', self.open_web)
            )),
            ('Run', (
                ('Run', self.open_run),
                ('Log', self.open_log)
            )),
            ('Report', (
                ('Report', self.open_report),
            )),
            ('help', ())
        )

        for _menu_name, _menu_actions in menu_def:

            _menu = menu.addMenu('&%s' % _menu_name)

            if not _menu_actions:
                continue

            for _action_name, _slot in _menu_actions:
                _action = _menu.addAction("&%s" % _action_name)
                _action.triggered.connect(_slot)

    def create_tools(self):
        """
        建立工具栏
        :return:
        """
        from OrcView.Main.Tools.Server import Server

        tools_server = self.addToolBar("Server")
        tools_server.addWidget(Server())
        tools_server.addSeparator()

    def close_tab(self):
        index = self.__wid_center.currentIndex()
        self.__wid_center.removeTab(index)

    def open_data(self):
        _view = ViewDataMag()
        self.__add_tab(_view)

    def open_batch(self):
        _view = ViewBatchDefMag()
        _view.sig_batch_det[dict].connect(self.open_case_select)
        self.__add_tab(_view)

    def open_case(self):
        _view = ViewCaseDefMag()
        _view.sig_case_det[dict].connect(self.open_step)
        self.__add_tab(_view)

    def open_case_select(self, p_data):
        _view = ViewBatchDetMag(p_data)
        self.__add_tab(_view)

    def open_step(self, p_data):
        _view = StepContainer(p_data)
        self.__add_tab(_view)

    def open_web(self):
        _view = ViewWebMain()
        self.__add_tab(_view)

    def open_run(self):
        _view = ViewRunMain()
        self.__add_tab(_view)

    def open_report(self):
        _view = ViewReportMain()
        self.__add_tab(_view)

    def open_log(self):
        self.__show_dock()

    def __add_tab(self, p_view):

        self.__wid_center.addTab(p_view, p_view.title)
        self.__wid_center.setCurrentWidget(p_view)

    def __show_dock(self):

        dock_log = DockLog()  # log widget
        self.addDockWidget(Qt.BottomDockWidgetArea, dock_log)

    def test(self):
        print "OK"
