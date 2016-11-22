# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Run.RunDef import ViewRunDef
from ReportDet import ViewReportDet


class ViewReportMain(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        _table_def_definition = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="pid", NAME=u"PID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="run_flag", NAME=u"名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="run_def_type", NAME=u"类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True)]

        self.title = u"执行"

        # View RunDef
        self.__wid_run_def = ViewRunDef(_table_def_definition)

        # View ReportDet
        self.__wid_report_det = ViewReportDet()

        # Search condition widget
        self.__wid_search_cond = ViewSearch(_table_def_definition)
        self.__wid_search_cond.create()

        # 底部 layout
        _layout_bottom = QHBoxLayout()
        _layout_bottom.addWidget(self.__wid_run_def)
        _layout_bottom.addWidget(self.__wid_report_det)

        # main layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addLayout(_layout_bottom)

        self.setLayout(_layout)

        self.__wid_run_def.sig_search.connect(self.search)
        self.__wid_run_def.sig_selected.connect(self.__wid_report_det.usr_refresh)
        # self.__wid_run_def.sig_run.connect(self.__wid_run_det.usr_refresh)

    def search(self):

        _cond = self.__wid_search_cond.get_cond()
        self.__wid_run_def.search(_cond)
