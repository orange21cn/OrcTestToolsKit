# coding=utf-8
from PySide.QtGui import QFormLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QDialog
from OrcView.Driver.Web.Page.PageSelector import PageSelector
from OrcView.Driver.Web.Widget.WidgetSelector import WidgetSelector
from OrcView.Lib.LibBaseWidget import WidgetCreator
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibMessage import OrcMessage
from OrcLib.LibType import WebItemModeType
from OrcLib.LibCmd import WebCmd
from OrcLib.LibCmd import DataCmd


class CmdCreator(QDialog):

    def __init__(self):

        QDialog.__init__(self)

        # 模式,检查/操作
        self._mode = ''

        # 命令,最终生成的字符串
        self._cmd = None

        # 按钮
        self._buttons = OrcButtons(
            [dict(id="submit", name=u"确定"),
             dict(id="cancel", name=u"取消")])

        # 布局
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # 点击按钮操作
        self._buttons.sig_clicked.connect(self._operate)

    def _operate(self, p_flag):
        """
        点击按钮后操作
        :return:
        """
        if 'submit' == p_flag:
            self._submit()
        elif 'cancel' == p_flag:
            self.close()
        else:
            pass

    def set_mode(self, p_mode):
        """
        设置模式,操作项/检查项
        :param p_mode:
        :return:
        """
        if p_mode in WebItemModeType.all():
            self._cmd.set_mode(p_mode)

    def _submit(self):
        """
        提交
        :return:
        """
        self.close()


class WebCmdCreator(CmdCreator):
    """
    命令生成控件
    """
    def __init__(self):

        CmdCreator.__init__(self)

        # 命令,最终生成的字符串
        self._cmd = WebCmd()

        # 控件类型
        self.__type_select = WidgetCreator.create_complex(self, 'OBJ_SELECT')

        # 控件信息输入
        self.__widget_input = WidgetCreator.create_line_text(self)
        self.__widget_input.setReadOnly(True)

        # 目标控件,拖拽时使用
        self.__widget_to = WidgetCreator.create_line_text(self)
        self.__widget_to.setReadOnly(True)

        # 操作信息输入 layout
        self.__operate_select = WidgetCreator.create_complex(self, 'OPE_SELECT')

        # form layout
        layout_form = QFormLayout()

        layout_form.addRow(u'对象类型:', self.__type_select)
        layout_form.addRow(u'控件:', self.__widget_input)
        layout_form.addRow(u'目标控件:', self.__widget_to)
        layout_form.addRow(u'操作:', self.__operate_select)

        layout_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # 主 layout
        self._layout.addLayout(layout_form)
        self._layout.addWidget(self._buttons)

        # 点击后弹出控件或页面选择信息
        self.__widget_input.clicked.connect(self._create_input)
        self.__widget_to.clicked.connect(self._create_to)

        # 类型变更, 页面/控件
        self.__type_select.currentIndexChanged.connect(self.__change_type)

        # 初始设置
        self.__change_type('PAGE')

    def set_mode(self, p_mode):
        """
        设置模式,操作项/检查项
        :param p_mode:
        :return:
        """
        if p_mode in WebItemModeType.all():
            self._cmd.set_mode(p_mode)
            self.__operate_select.set_sense(p_mode)

    def __change_type(self, p_data):
        """
        对象类型
        :param p_data:
        :return:
        """
        self.__widget_input.clear()
        self.__widget_to.clear()

        self._cmd.set_cmd_type(self.__type_select.get_data())

    def _create_input(self):
        """
        Show a select widget according to type
        :return:
        """
        if self._cmd.is_widget():
            self._cmd.set_widget_from_info(WidgetSelector().get_widget())

            self.__widget_input.set_data(self._cmd.get_flag())

            # 设置操作方式
            self.__operate_select.set_type(self._cmd.get_widget_type())

        elif self._cmd.is_page():

            self._cmd.set_page_from_info(PageSelector.static_get_data())

            self.__widget_input.set_data(self._cmd.get_flag())

            # 设置操作方式
            self.__operate_select.set_type('PAGE')

        elif self._cmd.is_window():
            # 设置操作方式
            self.__operate_select.set_type('WINDOW')

        else:
            pass

    def _create_to(self):
        """
        Show a select widget according to type
        :return:
        """
        if self._cmd.is_widget():
            self._cmd.set_widget_to_info(WidgetSelector().get_widget())

            self.__widget_to.set_data(self._cmd.get_flag('TO'))

            # 设置操作方式
            self.__operate_select.set_type('MULTI')

        else:
            pass

    def _submit(self):
        """
        提交
        :return:
        """
        if not self.__widget_input.get_data():
            OrcMessage.info(self, u'操作对象不可为空')
            return

        self._cmd.set_cmd_operation(self.__operate_select.get_data())

        self.close()

    @staticmethod
    def get_cmd(p_mode):
        """
        获取选择的页面
        :param p_mode:
        :return:
        """
        view = WebCmdCreator()
        view.set_mode(p_mode)
        view.exec_()
        return view._cmd


class DataCmdCreator(CmdCreator):
    """
    生成 sql 命令
    """
    def __init__(self):

        CmdCreator.__init__(self)

        # 命令
        self._cmd = DataCmd()

        # 显示数据标识
        self._wid_object = WidgetCreator.create_line_text()

        self._layout.addWidget(self._wid_object)
        self._layout.addWidget(self._buttons)

        # 设置标识,初始标识是自动生成的,可以修改
        self._wid_object.set_data(self._cmd.cmd_object)

    @staticmethod
    def get_cmd(p_mode):
        """
        获取选择的页面
        :param p_mode:
        :return:
        """
        view = DataCmdCreator()
        view.set_mode(p_mode)
        view.exec_()

        return view._cmd
