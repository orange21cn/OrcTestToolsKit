# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButton
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibControl import LibControl

from OrcView.Data.DataAdd import ViewCommonDataAdd


class BatchDefModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self)

        i_base_url = 'http://localhost:5000/BatchDef'
        _interface = {
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url,
            'usr_search': '%s/usr_search' % i_base_url
        }

        self.usr_set_interface(_interface)


class BatchDefControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewBatchDefMag(QWidget):

    sig_batch_det = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        _table_def = [
            dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="pid", NAME=u"父ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="batch_no", NAME=u"批编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=False, ESSENTIAL=False),
            dict(ID="batch_name", NAME=u"批名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=True),
            dict(ID="batch_desc", NAME=u"批描述", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=True, ADD=True, ESSENTIAL=False),
            dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
                 SEARCH=False, ADD=True, ESSENTIAL=False),
            dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False),
            dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
                 SEARCH=False, ADD=False, ESSENTIAL=False)]

        self.title = u"批管理"

        # Model
        self.__model = BatchDefModel()
        self.__model.usr_set_definition(_table_def)

        # Control
        _control = BatchDefControl(_table_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(_table_def)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Context menu
        _menu_def = [dict(NAME=u"增加", STR="sig_add"),
                     dict(NAME=u"删除", STR="sig_del"),
                     dict(NAME=u"增加数据", STR="sig_data")]

        _wid_display.create_context_menu(_menu_def)

        # Buttons widget
        _wid_buttons = ViewButton()
        _wid_buttons.enable_add()
        _wid_buttons.enable_delete()
        _wid_buttons.enable_modify()
        _wid_buttons.enable_search()
        _wid_buttons.create()

        # win_add
        self.__win_add = ViewAdd(_table_def)

        # win add data
        self.__win_data = ViewCommonDataAdd()

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_add.connect(self.__win_add.show)
        _wid_buttons.sig_delete.connect(self.__model.usr_delete)
        _wid_buttons.sig_modify.connect(self.__model.usr_editable)
        _wid_buttons.sig_search.connect(self.search)

        self.__win_add.sig_submit[dict].connect(self.add)
        _wid_display.doubleClicked[QModelIndex].connect(self.__batch_detail)

        _wid_display.sig_context.connect(self.__context)  # 右键菜单
        _wid_display.clicked.connect(self.__model.usr_set_current_data)

    def search(self):
        self.__model.usr_search(self.__wid_search_cond.get_cond())

    def add(self, p_data):
        self.__model.usr_add(p_data)

    def __batch_detail(self, p_index):

        if not self.__model.usr_get_editable():

            _id = self.__model.usr_get_node(p_index).content["id"]
            _no = self.__model.usr_get_node(p_index).content["batch_no"]
            _data = dict(id=_id, no=_no)

            self.sig_batch_det[dict].emit(_data)

    def __context(self, p_flag):

        if "sig_data" == p_flag:

            _path = self.__model.usr_get_current_data().content["batch_no"]
            self.__win_data.show()
            self.__win_data.set_type("BATCH")
            self.__win_data.set_id(_path)
