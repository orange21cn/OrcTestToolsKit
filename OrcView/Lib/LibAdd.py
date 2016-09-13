# coding=utf-8
from PySide.QtCore import SIGNAL
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QGridLayout
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QMessageBox
from PySide.QtGui import QPushButton
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcLib.LibCommon import is_null
from OrcView.Lib.LibView import create_editor


class ViewAdd(QWidget):
    """
    新增弹出框
    """
    sig_submit = OrcSignal([dict])
    sig_operate = OrcSignal()

    def __init__(self, p_def):

        QWidget.__init__(self)

        self.__fields = p_def
        self.__widgets = dict()
        _lay_inputs = QGridLayout()

        for t_index in range(len(self.__fields)):

            if not self.__fields[t_index]["ADD"]:
                continue

            _id = self.__fields[t_index]["ID"]
            _type = self.__fields[t_index]["TYPE"]
            _name = self.__fields[t_index]["NAME"]
            _def = dict(TYPE=_type, SOURCE="ADD", FLAG=_id)
            _ess = self.__fields[t_index]["ESSENTIAL"]
            _widget = create_editor(self, _def)

            self.__widgets[_id] = dict(
                TYPE=_type,
                NAME=_name,
                WIDGET=_widget,
                ESSENTIAL=_ess)

            if "OPERATE" == _type:
                _widget.sig_operate.connect(self.sig_operate.emit)

            if _ess:
                _label = QLabel("*" + _name + ":")
            else:
                _label = QLabel(_name + ":")

            _lay_inputs.addWidget(_label, t_index, 0)
            _lay_inputs.addWidget(self.__widgets[_id]["WIDGET"], t_index, 1)

        btn_submit = QPushButton(u"提交")
        btn_cancel = QPushButton(u"取消")

        lay_button = QHBoxLayout()
        lay_button.addStretch()
        lay_button.addWidget(btn_submit)
        lay_button.addWidget(btn_cancel)

        lay_main = QVBoxLayout()
        lay_main.addLayout(_lay_inputs)
        lay_main.addLayout(lay_button)

        self.setLayout(lay_main)

        self.connect(btn_cancel, SIGNAL('clicked()'), self.close)
        self.connect(btn_submit, SIGNAL('clicked()'), self.__submit)

    def set_data(self, p_id, p_data):
        self.__widgets[p_id]["WIDGET"].set_data(p_data)

    def get_data(self, p_id):
        return self.__widgets[p_id]["WIDGET"].get_data()

    def __submit(self):

        _res = dict()

        for t_id in self.__widgets:

            _res[t_id] = self.get_data(t_id)

            # Guarantee input is not null
            if self.__widgets[t_id]["ESSENTIAL"] and is_null(_res[t_id]):

                _message = u"%s不可以为空" % self.__widgets[t_id]["NAME"]
                _msg_box = QMessageBox(QMessageBox.Warning, "Alert", _message)
                _msg_box.exec_()

                return

        self.sig_submit[dict].emit(_res)
        self.close()
