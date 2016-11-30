# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibTree import ModelNewTree
from OrcView.Lib.LibControl import LibControl
from OrcView.Lib.LibViewDef import def_view_batch_def
from OrcView.Data.DataAdd import ViewDataAdd

from BatchService import BatchDefService


class BatchDefModel(ModelNewTree):

    def __init__(self):

        ModelNewTree.__init__(self)

        self.usr_set_service(BatchDefService())


class BatchDefControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewBatchDefMag(QWidget):

    sig_batch_det = OrcSignal(dict)

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"计划管理"

        self.__service = BatchDefService()

        # Model
        self.__model = BatchDefModel()
        self.__model.usr_set_definition(def_view_batch_def)

        # Control
        _control = BatchDefControl(def_view_batch_def)

        # Search condition widget
        self.__wid_search_cond = ViewSearch(def_view_batch_def)
        self.__wid_search_cond.create()

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Context menu
        _wid_display.create_context_menu([
            dict(NAME=u"增加", STR="sig_add"),
            dict(NAME=u"删除", STR="sig_del"),
            dict(NAME=u"增加数据", STR="sig_data"),
            dict(NAME=u"添加至运行", STR="sig_run")])

        # Buttons widget
        _wid_buttons = ViewButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="search", name=u"查询")
        ])

        # win_add
        self.__win_add = ViewAdd(def_view_batch_def)

        # win add data
        self.__win_data = ViewDataAdd()

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(self.__wid_search_cond)
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        # Connection
        _wid_buttons.sig_clicked.connect(self.__operate)

        self.__win_add.sig_submit[dict].connect(self.add)
        _wid_display.doubleClicked[QModelIndex].connect(self.__batch_detail)

        _wid_display.sig_context.connect(self.__context)  # 右键菜单
        _wid_display.clicked.connect(self.__model.usr_set_current_data)

    def search(self):
        self.__model.usr_search(self.__wid_search_cond.get_cond())

    def add(self, p_data):
        self.__model.usr_add(p_data)

    def __operate(self, p_flag):

        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            self.__model.usr_delete()
        elif "update" == p_flag:
            self.__model.usr_editable()
        elif "search" == p_flag:
            self.search()
        else:
            pass

    def __batch_detail(self, p_index):

        if not self.__model.usr_get_editable():

            _id = self.__model.usr_get_node(p_index).content["id"]
            _no = self.__model.usr_get_node(p_index).content["batch_no"]
            _data = dict(id=_id, no=_no)

            self.sig_batch_det[dict].emit(_data)

    def __context(self, p_flag):

        if "sig_data" == p_flag:

            _data = self.__model.usr_get_current_data()
            _path = _data.content["batch_no"]
            _id = _data.content["id"]

            self.__win_data.show()
            self.__win_data.set_type("BATCH")
            self.__win_data.set_path(_path)
            self.__win_data.set_id(_id)

        elif "sig_run" == p_flag:

            batch_id = self.__model.usr_get_current_data().content["id"]
            self.__service.add_to_run(batch_id)
