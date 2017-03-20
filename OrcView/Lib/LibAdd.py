# coding=utf-8
from functools import partial

from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QGridLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QMessageBox
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcLib.LibCommon import is_null
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibView import create_editor


class ViewAdd(QWidget):
    """
    新增弹出框
    """
    sig_submit = OrcSignal([dict])
    sig_operate = OrcSignal()
    sig_clicked = OrcSignal(str)

    def __init__(self, p_def):

        QWidget.__init__(self)

        self.__fields = p_def  # 控件定义
        self.widgets = dict()  # 控件

        _lay_inputs = QGridLayout()

        for _index in range(len(self.__fields)):

            if not self.__fields[_index]["ADD"]:
                continue

            _id = self.__fields[_index]["ID"]
            _type = self.__fields[_index]["TYPE"]
            _name = self.__fields[_index]["NAME"]
            _ess = self.__fields[_index]["ESSENTIAL"]

            _widget = create_editor(dict(TYPE=_type, SOURCE="ADD", FLAG=_id))

            self.widgets[_id] = dict(
                TYPE=_type,
                NAME=_name,
                WIDGET=_widget,
                ESSENTIAL=_ess)

            # ToBeDelete
            if "OPERATE" == _type:
                _widget.sig_operate.connect(self.sig_operate.emit)

            _widget.clicked.connect(partial(self.sig_clicked.emit, _id))

            _label = QLabel(("*" if _ess else " ") + _name + ":")

            _lay_inputs.addWidget(_label, _index, 0)
            _lay_inputs.addWidget(self.widgets[_id]["WIDGET"], _index, 1)

        buttons = OrcButtons([
            dict(id="submit", name=u"提交"),
            dict(id="cancel", name=u"取消")
        ])

        lay_main = QVBoxLayout()
        lay_main.addLayout(_lay_inputs)
        lay_main.addWidget(buttons)

        self.setLayout(lay_main)

        buttons.sig_clicked.connect(self.__operate)

        self.setStyleSheet(get_theme("Input"))

    def set_data(self, p_id, p_data):
        """
        设置数据
        :param p_id:
        :param p_data:
        :return:
        """
        self.widgets[p_id]["WIDGET"].set_data(p_data)

    def get_data(self, p_id):
        """
        获取数据
        :param p_id:
        :return:
        """
        return self.widgets[p_id]["WIDGET"].get_data()

    def set_enable(self, p_id, p_status):
        """
        设置控件可用/不可用
        :param p_id:
        :param p_status:
        :return:
        """
        self.widgets[p_id]["WIDGET"].setEnabled(p_status)

    def __operate(self, p_flag):

        if "submit" == p_flag:
            self.__submit()
        elif "cancel" == p_flag:
            self.close()
        else:
            pass

    def __submit(self):

        _res = dict()

        for t_id in self.widgets:

            _res[t_id] = self.get_data(t_id)

            # Guarantee input is not null
            if self.widgets[t_id]["ESSENTIAL"] and is_null(_res[t_id]):

                _message = u"%s不可以为空" % self.widgets[t_id]["NAME"]
                _msg_box = QMessageBox(QMessageBox.Warning, "Alert", _message)
                _msg_box.setStyleSheet(get_theme("Buttons"))
                _msg_box.exec_()

                return

        self.sig_submit[dict].emit(_res)
        self.close()
