# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QFormLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QDialog

from OrcView.Driver.Web.Page.PageDefView import PageDefSelector
from OrcView.Driver.Web.Widget.WidgetDefView import WidgetDefSelector
from OrcView.Lib.LibBaseWidget import WidgetCreator
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibMessage import OrcMessage
from OrcLib.LibCmd import WebCmd


class WebCmdCreator(QDialog):
    """
    命令生成控件
    """
    sig_submit = OrcSignal(dict)

    def __init__(self):

        QDialog.__init__(self)

        # 模式,检查/操作
        self._mode = ''

        # 命令,最终生成的字符串
        self._cmd = WebCmd()

        # 控件类型
        self.__type_select = WidgetCreator.create_complex(self, 'OBJ_SELECT')

        # 控件信息输入
        self.__widget_input = WidgetCreator.create_line_text(self)
        self.__widget_input.setReadOnly(True)

        # 操作信息输入 layout
        self.__operate_select = WidgetCreator.create_complex(self, 'OPE_SELECT')

        # 按钮
        buttons = OrcButtons(
            [dict(id="submit", name=u"确定"),
             dict(id="cancel", name=u"取消")])

        # form layout
        layout_form = QFormLayout()

        layout_form.addRow(u'对象类型', self.__type_select)
        layout_form.addRow(u'控件', self.__widget_input)
        layout_form.addRow(u'操作', self.__operate_select)

        layout_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # 主 layout
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_form)
        layout_main.addWidget(buttons)

        self.setLayout(layout_main)

        # 点击后弹出控件或页面选择信息
        self.__widget_input.clicked.connect(self.__show_select)

        # 类型变更, 页面/控件
        self.__type_select.currentIndexChanged.connect(self.__change_type)

        # 点击按钮
        buttons.sig_clicked.connect(self.__operate)

        # 初始设置
        self.__change_type('PAGE')

    def __operate(self, p_flag):
        """
        点击按钮操作
        :return:
        """
        if 'submit' == p_flag:
            self.__submit()
        elif 'cancel' == p_flag:
            self.close()
        else:
            pass

    def __set_mode(self, p_mode):
        """
        设置模式,操作项/检查项
        :param p_mode:
        :return:
        """
        self._cmd.set_mode(p_mode)
        self.__operate_select.set_sense(p_mode)

    def __change_type(self, p_data):
        """
        对象类型
        :param p_data:
        :return:
        """
        self.__widget_input.clear()
        self._cmd.set_cmd_type(self.__type_select.get_data())

    def __show_select(self):
        """
        Show a select widget according to type
        :return:
        """
        if self._cmd.is_widget():
            self._cmd.set_widget_info(WidgetDefSelector().get_widget())

            self.__widget_input.set_data(self._cmd.get_flag())

            # 设置操作方式
            self.__operate_select.set_type(self._cmd.get_widget_type())

        elif self._cmd.is_page():

            self._cmd.set_page_info(PageDefSelector.get_page())

            self.__widget_input.set_data(self._cmd.get_flag())

            # 设置操作方式
            self.__operate_select.set_type('PAGE')

        elif self._cmd.is_window():
            # 设置操作方式
            self.__operate_select.set_type('WINDOW')

        else:
            pass

    def __submit(self):
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
        view.__set_mode(p_mode)
        view.exec_()

        return view._cmd
