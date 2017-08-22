# coding=utf-8
from OrcView.Driver.Web.Widget.WidgetDetView import WidgetDetView
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QSplitter
from PySide.QtGui import QWidget
from PySide.QtGui import QSizePolicy

from OrcView.Driver.Web.Widget.WidgetDefView import WidgetDefView
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibViewDef import view_widget_def


class WidgetContainer(QWidget):

    sig_selected = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"控件"

        # Search condition widget
        self.__wid_search_cond = ViewSearch(view_widget_def, 2)

        # Column widget
        self.__wid_widget_def = WidgetDefView()
        self.__wid_widget_det = WidgetDetView()

        # Layout bottom
        _layout_bottom = QSplitter()
        _layout_bottom.addWidget(self.__wid_widget_def)
        _layout_bottom.addWidget(self.__wid_widget_det)

        _layout_bottom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout main
        _layout_main = QVBoxLayout()
        _layout_main.addWidget(self.__wid_search_cond)
        _layout_main.addWidget(_layout_bottom)

        _layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout_main)

        self.__wid_widget_def.sig_selected.connect(self.__wid_widget_det.set_widget)
        self.__wid_widget_def.sig_selected.connect(self.sig_selected.emit)
        self.__wid_widget_def.sig_search.connect(self.search_definition)
        self.__wid_widget_def.sig_delete.connect(self.__wid_widget_det.clean)

    def search_definition(self):
        """

        :return:
        """
        _cond = self.__wid_search_cond.get_cond()
        self.__wid_widget_def.search(_cond)
        self.__wid_widget_det.clean()
