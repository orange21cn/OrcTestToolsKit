# coding=utf-8
from PySide.QtCore import Qt
from PySide.QtCore import SIGNAL
from PySide.QtGui import QMainWindow
from PySide.QtGui import QTabWidget

from OrcLib import init_log
from OrcView.Batch.BatchDefView import BatchDefView
from OrcView.Batch.BatchDetView import BatchDetView
from OrcView.Case.Case.CaseView import CaseView
from OrcView.Case.Step.StepMain import StepContainer
from OrcView.Data.DataView import DataView
from OrcView.Driver.Web.WebMain import ViewWebMain
from OrcView.Lib.LibMain import DockCategory
from OrcView.Lib.LibMain import DockDetail
from OrcView.Lib.LibMain import DockLog
from OrcView.Lib.LibTheme import get_theme
from OrcView.Run.RunMain import RunMainView


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
        self.dock_detail = DockDetail()  # detail widget

        # center widget
        self.__wid_center = QTabWidget()
        self.setCentralWidget(self.__wid_center)

        self.__wid_center.setStyleSheet(get_theme("TabViewMain"))

        self.__wid_center.setTabsClosable(True)
        self.connect(self.__wid_center, SIGNAL("tabCloseRequested(int)"), self.close_tab)

        init_log()

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
            )),
            ('View', (
                (DockLog,),
            )),
            ('help', ())
        )

        for _menu_name, _menu_actions in menu_def:

            _menu = menu.addMenu('&%s' % _menu_name)

            if not _menu_actions:
                continue

            for _action_def in _menu_actions:

                if 1 == len(_action_def):
                    _widget = _action_def[0]()
                    self.addDockWidget(Qt.BottomDockWidgetArea, _widget)
                    _menu.addAction(_widget.toggleViewAction())
                    _widget.close()
                else:
                    _action = _menu.addAction("&%s" % _action_def[0])
                    _action.triggered.connect(_action_def[1])

    def create_tools(self):
        """
        建立工具栏
        :return:
        """
        from OrcView.Main.Tools.Server import ServerResource
        from OrcView.Main.Tools.Server import ServerRun
        from OrcView.Main.Tools.Server import ServerReport
        from OrcView.Main.Tools.Server import ServerDriver
        from OrcView.Main.Tools.Server import ServerDebug

        tools_server = self.addToolBar('Server')
        tools_server.addWidget(ServerResource())
        tools_server.addWidget(ServerRun())
        tools_server.addWidget(ServerReport())
        tools_server.addWidget(ServerDriver())
        tools_server.addWidget(ServerDebug())

        from OrcView.Main.Tools.Run import RunEnv
        from OrcView.Main.Tools.Run import RunBrowser

        tools_run = self.addToolBar('run')
        tools_run.addWidget(RunEnv())
        tools_run.addWidget(RunBrowser())

    def close_tab(self):
        index = self.__wid_center.currentIndex()
        self.__wid_center.removeTab(index)

    def open_data(self):
        _view = DataView()
        self.__add_tab(_view)

    def open_batch(self):
        _view = BatchDefView()
        _view.sig_batch_det[dict].connect(self.open_case_select)
        self.__add_tab(_view)

    def open_case(self):
        _view = CaseView()
        _view.sig_case_det[dict].connect(self.open_step)
        self.__add_tab(_view)

    def open_case_select(self, p_data):
        _view = BatchDetView(p_data)
        self.__add_tab(_view)

    def open_step(self, p_data):
        _view = StepContainer(p_data)
        self.__add_tab(_view)

    def open_web(self):
        _view = ViewWebMain()
        self.__add_tab(_view)

    def open_run(self):
        _view = RunMainView()
        self.__add_tab(_view)

    def open_log(self):
        self.__show_dock()

    def __add_tab(self, p_view):

        self.__wid_center.addTab(p_view, p_view.title)
        self.__wid_center.setCurrentWidget(p_view)

    def __show_dock(self):

        dock_log = DockLog()  # log widget
        self.addDockWidget(Qt.BottomDockWidgetArea, dock_log)
