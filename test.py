# coding=utf-8


class OrcPerformDef(QWidget):
    """
    测试步骤执行项输入框
    """
    sig_add_widget = OrcSignal()

    def __init__(self, p_type):

        QWidget.__init__(self)

        if "EDITOR" == p_type["SOURCE"]:
            self.resize(500, 300)

        # 控件标识
        _lab_inp = QLabel(u"控件标识:")
        _inp_def = dict(TYPE="LINETEXT",
                        SOURCE="ADD")
        self._input = create_editor(self, _inp_def)  # 对象显示框
        self._input.setEnabled(False)
        _btn_inp = QPushButton(u"选择")  # 对象输入按钮

        _lay_obj = QHBoxLayout()
        _lay_obj.addWidget(self._input)
        _lay_obj.addWidget(_btn_inp)

        # 操作输入
        _opt_def = dict(TYPE="SELECT",
                        SOURCE="ADD",
                        FLAG="item_operator_type")
        _lab_opt = QLabel(u"操作方式:")
        self.__wid_opt = create_editor(self, _opt_def)

        # 确定按钮
        _btn_submit = None
        if "ADD" == p_type["SOURCE"]:
            _btn_inp.clicked.connect(self.sig_add_widget.emit)

        # 主 layout
        _layout = QGridLayout()
        _layout.addWidget(_lab_inp, 0, 0)
        _layout.addLayout(_lay_obj, 0, 1)
        _layout.addWidget(_lab_opt, 1, 0)
        _layout.addWidget(self.__wid_opt, 1, 1)

        if _btn_submit is not None:
            _layout.addWidget(_btn_submit, 2, 1)

        self.setLayout(_layout)

    def get_data(self):
        """
        :return: {"OBJECT":"LOTTERY.NEW_BRANCH", "TYPE":"SUBMIT"}
        """
        _res = dict(OBJECT=self._input.text(),
                    TYPE=self.__wid_opt.get_data())
        return json.dumps(_res)

    def set_data(self, p_data):
        """
        :param p_data: {"OBJECT":"LOTTERY.NEW_BRANCH", "TYPE":"SUBMIT"}
        :return:
        """
        print p_data
        _obj, _opt = p_data.split(">")

        self._input.set_data(_obj)
        self.__wid_opt.set_data(_opt)


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
from OrcView.Driver.Web.WidgetSelect import ViewWidgetSelectMag
from OrcView.Lib.LibView import create_editor


class ViewAdd(QWidget):
    """
    新增弹出框
    """
    sig_submit = OrcSignal([dict])

    def __init__(self, p_def):

        QWidget.__init__(self)

        self.__fields_def = p_def

        self._inp_def = {}
        lay_inputs = QGridLayout()

        for t_index in range(len(self.__fields_def)):

            if not self.__fields_def[t_index]["ADD"]:
                continue

            _id = self.__fields_def[t_index]["ID"]
            _type = self.__fields_def[t_index]["TYPE"]
            _name = self.__fields_def[t_index]["NAME"]
            _def = dict(TYPE=_type, SOURCE="ADD", FLAG=_id)
            _ess = self.__fields_def[t_index]["ESSENTIAL"]
            _widget = create_editor(self, _def)

            self._inp_def[_id] = dict(
                TYPE=_type,
                NAME=_name,
                WIDGET=_widget,
                ESSENTIAL=_ess)

            if "OPERATE" == _type:
                self._inp = ViewWidgetSelectMag()
                _widget.sig_add_widget.connect(self._inp.show)
                self._inp.sig_selected.connect(self.set_widget_path)

            if _ess:
                _label = QLabel("*" + _name + ":")
            else:
                _label = QLabel(_name + ":")

            lay_inputs.addWidget(_label, t_index, 0)
            lay_inputs.addWidget(self._inp_def[_id]["WIDGET"], t_index, 1)

        btn_submit = QPushButton(u"提交")
        btn_cancel = QPushButton(u"取消")

        lay_button = QHBoxLayout()
        lay_button.addStretch()
        lay_button.addWidget(btn_submit)
        lay_button.addWidget(btn_cancel)

        lay_main = QVBoxLayout()
        lay_main.addLayout(lay_inputs)
        lay_main.addLayout(lay_button)

        self.setLayout(lay_main)

        self.connect(btn_cancel, SIGNAL('clicked()'), self.close)
        self.connect(btn_submit, SIGNAL('clicked()'), self.__submit)

    def set_widget_path(self, p_data):
        self._inp_def["item_operate"]["WIDGET"]._input.set_data(p_data["path"])

    def __submit(self):

        _res = {}

        for t_id in self._inp_def:

            _res[t_id] = self._inp_def[t_id]["WIDGET"].get_data()

            # Guarantee input is not null
            if self._inp_def[t_id]["ESSENTIAL"] and is_null(_res[t_id]):
                _message = u"%s不可以为空" % self._inp_def[t_id]["NAME"]
                _msg_box = QMessageBox(QMessageBox.Warning, "Alert", _message)
                _msg_box.exec_()

                return

        self.sig_submit[dict].emit(_res)
        self.close()
