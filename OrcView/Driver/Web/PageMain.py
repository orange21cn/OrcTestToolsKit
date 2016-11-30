# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout

from OrcView.Driver.Web.PageDef import ViewPageDefMag
from OrcView.Driver.Web.PageDet import ViewPageDetMag
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibViewDef import def_view_page_def


class PageContainer(QWidget):

    sig_selected = OrcSignal(str)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"页面"

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_page_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Column widget
        self.__wid_page_def = ViewPageDefMag()
        self.__wid_page_det = ViewPageDetMag()

        # Bottom layout
        _layout_bottom = QHBoxLayout()
        _layout_bottom.addWidget(self.__wid_page_def)
        _layout_bottom.addWidget(self.__wid_page_det)

        # Main layout
        _layout_main = QVBoxLayout()
        _layout_main.addWidget(self.__wid_search_cond)
        _layout_main.addLayout(_layout_bottom)

        _layout_main.setContentsMargins(0, 0, 0, 0)
        _layout_main.setSpacing(0)

        self.setLayout(_layout_main)

        self.__wid_page_def.sig_selected.connect(self.__wid_page_det.set_page_id)
        self.__wid_page_def.sig_search.connect(self.search_definition)
        self.__wid_page_def.sig_delete.connect(self.__wid_page_det.clean)
        self.__wid_page_det.sig_selected[str].connect(self.sig_selected.emit)

    def search_definition(self):
        _cond = self.__wid_search_cond.get_cond()
        self.__wid_page_def.search(_cond)
        self.__wid_page_det.clean()
