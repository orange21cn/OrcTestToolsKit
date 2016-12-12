# coding=utf-8
from PySide.QtGui import QMainWindow
from PySide.QtGui import QTabWidget
from PySide.QtCore import SIGNAL
from PySide.QtCore import Qt

from OrcView.Lib.LibMain import DockCategory
from OrcView.Lib.LibMain import DockDetail
from OrcView.Lib.LibMain import DockBottom
from OrcView.Lib.LibTheme import get_theme
from OrcView.Batch.BatchDef import ViewBatchDefMag
from OrcView.Batch.BatchDet import ViewBatchDetMag
from OrcView.Case.CaseDef import ViewCaseDefMag
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

        # Menu
        main_menu = self.menuBar()

        self.create = main_menu.addMenu('&Create')
        self.run = main_menu.addMenu('&Run')
        self.report = main_menu.addMenu('&Report')
        self.help = main_menu.addMenu('&Help')

        action_batch = self.create.addAction('&Batch')
        action_case = self.create.addAction('&Case')
        action_data = self.create.addAction('&Data')
        action_web = self.create.addAction('&Web')
        action_run = self.run.addAction('&Run')
        action_test = self.run.addAction('&Test')
        action_report = self.report.addAction('&Report')

        self.connect(action_batch, SIGNAL('triggered()'), self.open_batch)
        self.connect(action_case, SIGNAL('triggered()'), self.open_case)
        self.connect(action_test, SIGNAL('triggered()'), self.open_test)
        self.connect(action_data, SIGNAL('triggered()'), self.open_data)
        self.connect(action_web, SIGNAL('triggered()'), self.open_web_object)
        self.connect(action_run, SIGNAL('triggered()'), self.open_run)
        self.connect(action_report, SIGNAL('triggered()'), self.open_report)

        # Dock
        self.dock_category = DockCategory()  # category widget
        self.dock_log = DockBottom()  # log widget
        self.dock_detail = DockDetail()  # detail widget

        self.__dock_displayed = False

        # center widget
        self.__wid_center = QTabWidget()
        self.setCentralWidget(self.__wid_center)

        self.__wid_center.setStyleSheet(get_theme("TabViewMain"))

        self.__wid_center.setTabsClosable(True)
        self.connect(self.__wid_center, SIGNAL("tabCloseRequested(int)"), self.close_tab)

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

    def open_web_object(self):
        _view = ViewWebMain()
        self.__add_tab(_view)

    def open_run(self):
        _view = ViewRunMain()
        self.__add_tab(_view)

    def open_report(self):
        _view = ViewReportMain()
        self.__add_tab(_view)

    def open_test(self):
        self.__show_dock()

    def __add_tab(self, p_view):

        self.__wid_center.addTab(p_view, p_view.title)
        self.__wid_center.setCurrentWidget(p_view)

    def __show_dock(self):

        if not self.__dock_displayed:

            self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_log)
            # self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_category)
            # self.addDockWidget(Qt.RightDockWidgetArea, self.dock_detail)
            pass
