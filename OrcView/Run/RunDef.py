# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import Signal as OrcSignal
from PySide.QtCore import QThread

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibSearch import ViewButtons
from OrcView.Lib.LibTree import ModelNewTree
from OrcView.Lib.LibControl import LibControl
from RunDefService import RunDefService


class RunDefModel(ModelNewTree):

    def __init__(self):

        ModelNewTree.__init__(self)

        service = RunDefService()
        self.usr_set_service(service)


class RunDefControl(LibControl):

    def __init__(self, p_def):

        LibControl.__init__(self, p_def)


class ViewRunDef(QWidget):

    sig_search = OrcSignal()
    sig_selected = OrcSignal(str)
    sig_run = OrcSignal()

    def __init__(self, p_def):

        QWidget.__init__(self)

        self.__table_def = p_def

        self.title = u"执行列表"
        self.__service = RunDefService()
        self.__threads = []

        # Model
        self.__model = RunDefModel()
        self.__model.usr_set_definition(self.__table_def)

        # Control
        _control = RunDefControl(self.__table_def)

        # Data result display widget
        _wid_display = ViewTree()
        _wid_display.set_model(self.__model)
        _wid_display.set_control(_control)

        # Buttons window
        _btn_definition = [
            dict(id="add", name=u'增加'),
            dict(id="delete", name=u"删除"),
            dict(id="search", name=u'查询'),
            dict(id="run", name=u"执行")
        ]
        _wid_buttons = ViewButtons(_btn_definition)
        _wid_buttons.align_back()

        # Layout
        _layout = QVBoxLayout()
        _layout.addWidget(_wid_display)
        _layout.addWidget(_wid_buttons)

        self.setLayout(_layout)

        _wid_display.clicked.connect(self.__model.usr_set_current_data)
        _wid_buttons.sig_clicked.connect(self.__operate)
        _wid_display.clicked.connect(self.select)

    def select(self, p_index):

        _node = self.__model.usr_get_node(p_index)
        _node_content = _node.content
        _node_flag = _node_content["run_flag"]
        _node_pid = _node_content["pid"]

        if _node_pid is None:
            return None

        _parent_content = _node.parent.content
        _parent_type = _parent_content["run_def_type"]
        _parent_id = _parent_content["id"]

        _file = "%s_%s/%s" % (_parent_type, _parent_id, _node_flag)

        self.sig_selected.emit(_file)

    def search(self, p_cond):
        self.__model.usr_search(p_cond)

    def __operate(self, p_flg):

        if "add" == p_flg:
            # {id, run_def_type, result}
            data = self.__model.usr_get_current_data()

            if data is None:
                return

            self.__model.usr_add(dict(run_def_type=data.content["run_def_type"]))

        elif "delete" == p_flg:
            self.__model.usr_delete()

        elif "search" == p_flg:
            self.sig_search.emit()

        elif "run" == p_flg:

            self.sig_run.emit()

            item_data = self.__model.usr_get_current_data()

            if item_data is not None:
                _id = item_data.content["id"]
                _pid = item_data.content["pid"]

                if _pid is None:
                    return

                _thread_run = RunThread()
                _thread_run.setup(_pid, _id)
                _thread_run.start()

                self.__threads.append(_thread_run)

        else:
            pass


class RunThread(QThread):

    def __init__(self):

        QThread.__init__(self)

        self.__service = RunDefService()

        self.__pid = None
        self.__id = None

    def setup(self, p_pid, p_id):

        self.__pid = p_pid
        self.__id = p_id

    def run(self, *args, **kwargs):

        self.__service.usr_run(self.__pid, self.__id)