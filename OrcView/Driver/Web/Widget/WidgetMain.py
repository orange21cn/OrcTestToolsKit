# coding=utf-8
from OrcView.Driver.Web.Widget.WidgetDetView import WidgetDetView
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcView.Driver.Web.Widget.WidgetDefView import WidgetDefView
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibViewDef import def_view_widget_def


class WidgetContainer(QWidget):

    sig_selected = OrcSignal(str)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"控件"

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_widget_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Column widget
        self.__wid_widget_def = WidgetDefView()
        self.__wid_widget_det = WidgetDetView()

        # Layout bottom
        _layout_bottom = QHBoxLayout()
        _layout_bottom.addWidget(self.__wid_widget_def)
        _layout_bottom.addWidget(self.__wid_widget_det)

        # Layout main
        _layout_main = QVBoxLayout()
        _layout_main.addWidget(self.__wid_search_cond)
        _layout_main.addLayout(_layout_bottom)

        _layout_main.setContentsMargins(0, 0, 0, 0)
        _layout_main.setSpacing(0)

        self.setLayout(_layout_main)

        self.__wid_widget_def.sig_selected.connect(self.__wid_widget_det.set_widget_id)
        self.__wid_widget_def.sig_selected.connect(self.sig_selected.emit)
        self.__wid_widget_def.sig_search.connect(self.search_definition)
        self.__wid_widget_def.sig_delete.connect(self.__wid_widget_det.clean)

    def search_definition(self):
        _cond = self.__wid_search_cond.get_cond()
        self.__wid_widget_def.search(_cond)
        self.__wid_widget_det.clean()
