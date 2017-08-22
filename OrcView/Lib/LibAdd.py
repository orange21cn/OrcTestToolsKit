# coding=utf-8
from functools import partial

from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QGridLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QMessageBox
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QFormLayout
from PySide.QtGui import QWidget

from OrcLib.LibCommon import is_null
from OrcLib.LibProgram import OrcFactory
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibView import WidgetFactory
from OrcView.Lib.LibMessage import OrcMessage

from OrcView.Lib.LibShell import OrcBasicSelector
from OrcView.Lib.LibViewDef import ViewDefinition


class ViewAdd(QWidget):
    """
    新增弹出框
    """
    sig_submit = OrcSignal([dict])
    sig_clicked = OrcSignal(str)

    def __init__(self, p_def):

        QWidget.__init__(self)

        # 控件定义
        self.__fields = p_def

        # 控件
        self.widgets = dict()

        layout_input = QGridLayout()

        for _index in range(len(self.__fields)):

            if not self.__fields[_index]["ADD"]:
                continue

            _id = self.__fields[_index]["ID"]
            _type = self.__fields[_index]["TYPE"]
            _name = self.__fields[_index]["NAME"]
            _ess = self.__fields[_index]["ESSENTIAL"]

            _widget = WidgetFactory.create_widget(dict(TYPE=_type, SOURCE="ADD", FLAG=_id))

            self.widgets[_id] = dict(
                TYPE=_type,
                NAME=_name,
                WIDGET=_widget,
                ESSENTIAL=_ess)

            _widget.clicked.connect(partial(self.sig_clicked.emit, _id))

            _label = QLabel(("*" if _ess else " ") + _name + ":")

            layout_input.addWidget(_label, _index, 0)
            layout_input.addWidget(self.widgets[_id]["WIDGET"], _index, 1)

        buttons = OrcButtons([
            dict(id="submit", name=u"提交"),
            dict(id="cancel", name=u"取消")
        ])

        lay_main = QVBoxLayout()
        lay_main.addLayout(layout_input)
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

    def clean_data(self, p_id):
        """
        清空数据
        :param p_id:
        :return:
        """
        self.widgets[p_id]['WIDGET'].clear()  # todo 可能有问题对于不同的控件应该有针对性的方法

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


class ViewNewAdd(OrcBasicSelector):
    """
    新增弹出框
    """
    # 提交信号
    sig_submit = OrcSignal([dict])

    # 输入控件点击信号
    sig_clicked = OrcSignal(str)

    def __init__(self, p_def):
        """
        :param p_def:
        :type p_def:
        :return:
        """
        OrcBasicSelector.__init__(self)

        # 控件定义
        self._def = ViewDefinition(p_def)

        # 主控件
        self.display = QWidget()

        # 控件字典aa
        self._widgets = OrcFactory.create_ordered_dict()

        # 主控件布局
        layout_input = QFormLayout()
        layout_input.setContentsMargins(0, 0, 0, 0)
        layout_input.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.display.setLayout(layout_input)

        # 生成主控件
        for _key in self._def.add_keys:

            _field = self._def.field(_key)
            _widget = WidgetFactory.create_widget(dict(TYPE=_field.type, SOURCE="ADD", FLAG=_field.id))

            self._widgets.append(_key, _widget)
            layout_input.addRow(("*" if _field.essential else " ") + _field.name + ":", _widget)

            _widget.clicked.connect(partial(self.sig_clicked.emit, _key))

        # 样式
        self.setStyleSheet(get_theme("Input"))

        # +---- Connection ----+
        self.sig_clicked.connect(self._action)

        # 初始化界面
        self.init_view()

    def widget(self, p_id):
        """
        控件
        :param p_id:
        :return:
        """
        return self._widgets.value(p_id)

    def set_data(self, p_id, p_data):
        """
        设置数据
        :param p_id:
        :param p_data:
        :return:
        """
        self._widgets.value(p_id).set_data(p_data)

    def get_data(self, p_key=None):
        """
        获取数据
        :param p_key:
        :return:
        """
        if p_key is not None:
            return self._widgets.value(p_key).get_data()

        result = dict()
        for _key in self._widgets.keys():
            result[_key] = self._widgets.value(_key).get_data()

        return result

    def clean_data(self, p_key=None):
        """
        清空数据
        :param p_key:
        :return:
        """
        # todo 可能有问题对于不同的控件应该有针对性的方法
        if p_key is not None:
            self._widgets.value(p_key).clear()
            return

        for _key in self._widgets.keys():
            self.widget(_key).clear()

    def set_enable(self, p_id, p_status):
        """
        设置控件可用/不可用
        :param p_id:
        :param p_status:
        :return:
        """
        self._widgets.value(p_id).setEnabled(p_status)

    def _operate(self, p_flag):
        """
        点击按钮操作
        :param p_flag:
        :return:
        """
        if "submit" == p_flag:
            self._submit()
        elif "cancel" == p_flag:
            self.close()
        else:
            pass

    def _submit(self):
        """
        提交
        :return:
        """
        result = self.get_data()

        for _key in self._def.essential_keys:
            if (_key not in result) or is_null(result[_key]):
                OrcMessage.info(self, u'%s不可以为空' % self._def.field(_key).name)
                return

        self._data = result

        self.sig_submit.emit(result)
        self.close()

    def _action(self, p_flag):
        """
        控件被点击后操作,给继承该类的控件用
        :return:
        """
        pass
