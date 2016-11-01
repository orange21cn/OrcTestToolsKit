# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout

from OrcView.Driver.Web.PageDef import ViewPageDefMag
from OrcView.Driver.Web.PageDet import ViewPageDetMag
from OrcView.Lib.LibSearch import ViewSearch


class PageContainer(QWidget):

    sig_selected = OrcSignal(str)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"页面管理"

        _table_page_def = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="page_flag", NAME=u"页面标识", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="page_desc", NAME=u"页面描述", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        _table_page_det = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="page_id", NAME=u"页面ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="page_env", NAME=u"环境", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="page_url", NAME=u"URL", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        # Search condition widget
        self.__wid_search_cond = ViewSearch(_table_page_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Column widget
        self.__wid_page_def = ViewPageDefMag(_table_page_def)
        self.__wid_page_det = ViewPageDetMag(_table_page_det)

        # Bottom layout
        _layout_bottom = QHBoxLayout()
        _layout_bottom.addWidget(self.__wid_page_def)
        _layout_bottom.addWidget(self.__wid_page_det)

        # Main layout
        _layout_main = QVBoxLayout()
        _layout_main.addWidget(self.__wid_search_cond)
        _layout_main.addLayout(_layout_bottom)

        _layout_main.setContentsMargins(0, 0, 0, 0)
        _layout_main.setSpacing(1)

        self.setLayout(_layout_main)

        self.__wid_page_def.sig_selected.connect(self.__wid_page_det.set_page_id)
        self.__wid_page_def.sig_search.connect(self.search_definition)
        self.__wid_page_def.sig_delete.connect(self.__wid_page_det.clean)
        self.__wid_page_det.sig_selected[str].connect(self.sig_selected.emit)

    def search_definition(self):
        _cond = self.__wid_search_cond.get_cond()
        self.__wid_page_def.search(_cond)
        self.__wid_page_det.clean()
