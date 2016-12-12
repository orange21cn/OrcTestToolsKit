# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QSplitter

from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Run.RunDef import ViewRunDef
from OrcView.Lib.LibViewDef import def_view_run_def
from ReportDet import ViewReportDet


class ViewReportMain(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"执行"

        # View RunDef
        self.__wid_run_def = ViewRunDef()

        # View ReportDet
        self.__wid_report_det = ViewReportDet()

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_run_def)
        self.__wid_search_cond.create()

        # 底部 layout
        _layout_bottom = QSplitter()
        _layout_bottom.addWidget(self.__wid_run_def)
        _layout_bottom.addWidget(self.__wid_report_det)

        # main layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_layout_bottom)

        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)

        self.__wid_run_def.sig_search.connect(self.search)
        self.__wid_run_def.sig_selected.connect(self.__wid_report_det.usr_refresh)

    def search(self):

        _cond = self.__wid_search_cond.get_cond()
        self.__wid_run_def.search(_cond)
