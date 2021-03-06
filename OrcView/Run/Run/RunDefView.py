# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibMessage import OrcMessage

from .RunDefModel import RunDefModel


class RunDefControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'RunDef')


class RunDefView(QWidget):

    sig_search = OrcSignal()
    sig_selected = OrcSignal(str)
    sig_start = OrcSignal()

    def __init__(self):

        QWidget.__init__(self)

        self.title = u"执行列表"
        self.__threads = []

        # Data result display widget
        self.display = ViewTree(RunDefModel, RunDefControl)

        # Buttons window
        self.__wid_buttons = OrcButtons([
            dict(id="add", name=u'增加'),
            dict(id="delete", name=u"删除"),
            dict(id="search", name=u'查询'),
            dict(id="run", name=u"执行"),
            dict(id="stop", name=u"停止")
        ])

        # Layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.display)
        layout_main.addWidget(self.__wid_buttons)

        self.setLayout(layout_main)

        layout_main.setContentsMargins(0, 0, 0, 0)

        # 点击按钮操作
        self.__wid_buttons.sig_clicked.connect(self.operate)

        # 点击选中事件
        self.display.clicked.connect(self.select)

    def select(self, p_index):
        """
        查询
        :param p_index:
        :return:
        """
        _node = self.display.model.node(p_index)
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

        self.__wid_buttons.set_disable('stop')

    def search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        self.display.model.mod_search(p_cond)

    def operate(self, p_flg):
        """
        点击按钮操作
        :param p_flg:
        :return:
        """
        if 'add' == p_flg:
            # {id, run_def_type, result}
            data = self.display.model.mod_get_current_data()
            if data:
                self.display.model.mod_add(dict(run_def_type=data["run_def_type"]))

        elif 'delete' == p_flg:
            if OrcMessage.question(self, u"确认删除"):
                self.display.model.mod_delete()

        elif 'search' == p_flg:
            self.sig_search.emit()

        elif 'run' == p_flg:

            self.sig_start.emit()

            item_data = self.display.model.mod_get_current_data()

            if item_data is not None:

                _id = item_data["id"]
                _pid = item_data["pid"]

                if _pid is None:
                    return

                # 运行
                self.display.model.service_run(_pid, _id)

                # 更改按钮状态
                # self.btn_status_start()

        elif 'stop' == p_flg:
            # 停止
            self.display.model.service_stop()

            # 按钮状态停止
            # self.btn_status_stop()

        else:
            pass

    def btn_status_start(self):
        """
        按钮运行状态
        :return:
        """
        self.__wid_buttons.set_disable('add')
        self.__wid_buttons.set_disable('delete')
        self.__wid_buttons.set_disable('search')
        self.__wid_buttons.set_disable('run')
        self.__wid_buttons.set_enable('stop')

    def btn_status_stop(self):
        """
        按钮停止状态
        :return:
        """
        self.__wid_buttons.set_enable('add')
        self.__wid_buttons.set_enable('delete')
        self.__wid_buttons.set_enable('search')
        self.__wid_buttons.set_enable('run')
        self.__wid_buttons.set_disable('stop')
