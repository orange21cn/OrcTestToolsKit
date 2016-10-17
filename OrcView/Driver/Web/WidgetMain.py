# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout

from OrcView.Driver.Web.WidgetDef import ViewWidgetDefMag
from OrcView.Driver.Web.WidgetDet import ViewWidgetDetMag
from OrcView.Lib.LibSearch import ViewSearch


class WidgetContainer(QWidget):

    sig_selected = OrcSignal(str)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"控件管理"

        _table_widget_def = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="pid", NAME=u"父ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="widget_flag", NAME=u"控件标识", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="widget_path", NAME=u"控件路径", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="widget_type", NAME=u"控件类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="widget_desc", NAME=u"控件描述", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        _table_widget_det = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="widget_id", NAME=u"控件ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="widget_order", NAME=u"属性顺序", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=False, ESSENTIAL=False),
            dict(ID="widget_attr_type", NAME=u"属性类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="widget_attr_value", NAME=u"属性值", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="widget_desc", NAME=u"属性描述描述", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        # Search condition widget
        self.__wid_search_cond = ViewSearch(_table_widget_def)
        self.__wid_search_cond.set_col_num(2)
        self.__wid_search_cond.create()

        # Column widget
        self.__wid_widget_def = ViewWidgetDefMag(_table_widget_def)
        self.__wid_widget_det = ViewWidgetDetMag(_table_widget_det)

        # Layout bottom
        _layout_bottom = QHBoxLayout()
        _layout_bottom.addWidget(self.__wid_widget_def)
        _layout_bottom.addWidget(self.__wid_widget_det)

        # Layout main
        _layout_main = QVBoxLayout()
        _layout_main.addWidget(self.__wid_search_cond)
        _layout_main.addLayout(_layout_bottom)

        self.setLayout(_layout_main)

        self.__wid_widget_def.sig_selected.connect(self.__wid_widget_det.set_widget_id)
        self.__wid_widget_def.sig_selected.connect(self.sig_selected.emit)
        self.__wid_widget_def.sig_search.connect(self.search_definition)
        self.__wid_widget_def.sig_delete.connect(self.__wid_widget_det.clean)

    def search_definition(self):
        _cond = self.__wid_search_cond.get_cond()
        self.__wid_widget_def.search(_cond)
        self.__wid_widget_det.clean()
