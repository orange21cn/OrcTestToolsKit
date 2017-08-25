# coding=utf-8
from functools import partial

from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QFormLayout
from PySide.QtGui import QWidget

from OrcLib.LibCommon import is_null
from OrcLib.LibProgram import OrcFactory
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibView import WidgetFactory
from OrcView.Lib.LibMessage import OrcMessage

from OrcView.Lib.LibShell import OrcDialogView
from OrcView.Lib.LibViewDef import WidgetDefinition


class BaseAdder(OrcDialogView):
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
        OrcDialogView.__init__(self)

        # 控件定义
        self._def = WidgetDefinition(p_def)

        # 主控件
        self.view = QWidget()
        self.main.display = self.view

        # 控件字典aa
        self._widgets = OrcFactory.create_ordered_dict()

        # 主控件布局
        layout_input = QFormLayout()
        layout_input.setContentsMargins(0, 0, 0, 0)
        layout_input.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.view.setLayout(layout_input)

        # 生成主控件
        for _key in self._def.add_keys:

            _field = self._def.field(_key)
            _widget = WidgetFactory.create_widget(dict(TYPE=_field.type, SOURCE="ADD", FLAG=_field.id))

            self._widgets.append(_key, _widget)
            layout_input.addRow(("*" if _field.essential else " ") + _field.name + ":", _widget)

            _widget.clicked.connect(partial(self.sig_clicked.emit, _key))

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_submit", name=u"新增"),
            dict(id="act_cancel", name=u"取消")]

        # 样式
        self.setStyleSheet(get_theme("Input"))

        # +---- Connection ----+
        self.sig_clicked.connect(self._action)

        # 初始化界面
        self.main.init_view()

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

    def act_submit(self):
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
