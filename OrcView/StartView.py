# coding=utf-8

from PySide.QtGui import QMainWindow
from PySide.QtGui import QTabWidget
from PySide.QtCore import Qt
from PySide.QtCore import SIGNAL

from OrcView.Lib.LibMain import DockCategory
from OrcView.Lib.LibMain import DockDetail
from OrcView.Lib.LibMain import DockLog
from OrcView.Batch.BatchDef import ViewBatchDefMag
from OrcView.Batch.BatchDet import ViewBatchDetMag
from OrcView.Case.CaseDef import ViewCaseDefMag
from OrcView.Case.StepMain import StepContainer
from OrcView.Data.DataDef import ViewDataMag
from OrcView.Driver.Web.WebMain import ViewWebMain
from OrcView.Driver.Web.WidgetMain import WidgetContainer


class StartView(QMainWindow):

    def __init__(self):

        super(StartView, self).__init__()

        self.setWindowTitle("hello")
        self.resize(1024, 768)

        # Menu
        main_menu = self.menuBar()
        self.file = main_menu.addMenu('&File')
        self.create = main_menu.addMenu('&Create')
        self.run = main_menu.addMenu('&Run')
        self.trace = main_menu.addMenu('&Trace')
        self.report = main_menu.addMenu('&Report')
        self.report = main_menu.addMenu('&Window')
        self.help = main_menu.addMenu('&Help')

        action_batch = self.create.addAction('&Batch')
        action_case = self.create.addAction('&Case')
        action_data = self.create.addAction('&Data')
        # action_page = self.create.addAction('&Page')
        action_web_object = self.create.addAction('&Web')
        action_test = self.create.addAction('&Test')

        action_open = self.file.addAction('Open')
        action_save = self.file.addAction('Save')
        action_close = self.file.addAction("Close")

        self.connect(action_batch, SIGNAL('triggered()'), self.open_batch)
        self.connect(action_case, SIGNAL('triggered()'), self.open_case)
        self.connect(action_test, SIGNAL('triggered()'), self.open_test)
        self.connect(action_data, SIGNAL('triggered()'), self.open_data)
        # self.connect(action_page, SIGNAL('triggered()'), self.open_page)
        self.connect(action_web_object, SIGNAL('triggered()'), self.open_web_object)
        self.connect(action_close, SIGNAL('triggered()'), self.close)

        # Dock
        self.dock_category = DockCategory()  # category widget
        self.dock_log = DockLog()  # log widget
        self.dock_detail = DockDetail()  # detail widget

        self.__dock_displayed = False

        # center widget
        self.__wid_center = QTabWidget()
        self.setCentralWidget(self.__wid_center)

    def open_data(self):
        _view = ViewDataMag()
        self.__wid_center.addTab(_view, _view.title)
        self.__show_dock()

    def open_batch(self):

        _view = ViewBatchDefMag()

        _view.sig_batch_det[dict].connect(self.open_case_select)
        self.__wid_center.addTab(_view, _view.title)

        self.__show_dock()

    def open_case(self):
        _view = ViewCaseDefMag()
        _view.sig_case_det[dict].connect(self.open_step)
        self.__wid_center.addTab(_view, _view.title)
        self.__show_dock()

    def open_case_select(self, p_data):
        _view = ViewBatchDetMag(p_data)
        self.__wid_center.addTab(_view, _view.title)
        self.__show_dock()

    def open_step(self, p_data):
        _view = StepContainer(p_data)
        self.__wid_center.addTab(_view, _view.title)
        self.__show_dock()

    # def open_page(self):
    #     _view = PageContainer()
    #     self.__wid_center.addTab(_view, _view.title)
    #     self.__show_dock()

    def open_web_object(self):
        _view = ViewWebMain()
        self.__wid_center.addTab(_view, _view.title)
        self.__show_dock()

    def open_test(self):
        pass

    def __show_dock(self):

        if not self.__dock_displayed:

            self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_log)
            self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_category)
            self.addDockWidget(Qt.RightDockWidgetArea, self.dock_detail)
