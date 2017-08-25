# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QGroupBox
from PySide.QtGui import QFormLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QStackedWidget

from OrcLib.LibProgram import orc_singleton
from OrcLib.LibCmd import OrcCmd
from OrcLib.LibCmd import OrcDriverCmd
from OrcLib.LibCmd import WebCmd
from OrcLib.LibType import WebObjectType
from OrcLib.LibNet import OrcSocketResource

from OrcView.Lib.LibBaseWidget import WidgetCreator
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTheme import get_theme


@orc_singleton
class WebDebug(QWidget):
    """
    WEB 调试控件
    """
    def __init__(self):

        QWidget.__init__(self)

        # 页面调试控件
        self._wid_debug_page = PageDebug()

        # 窗口调试控件
        self._wid_debug_window = WindowDebug()

        # 控件调试控件
        self._wid_debug_widget = WidgetDebug()

        # 调试控件
        self._wid_debug = QStackedWidget()
        self._wid_debug.addWidget(self._wid_debug_page)
        self._wid_debug.addWidget(self._wid_debug_window)
        self._wid_debug.addWidget(self._wid_debug_widget)

        layout_top = QVBoxLayout()
        layout_top.addWidget(self._wid_debug)

        group_top = QGroupBox()
        group_top.setLayout(layout_top)

        # 结果
        self._wid_result = WidgetCreator.create_select('result', True)
        self._wid_result.setEnabled(False)

        # 注释
        self._wid_comment = WidgetCreator.create_text_area(self)

        # 开始按钮
        btn_debug = OrcButtons([dict(id="debug", name=u"调试")])

        # 底部布局
        layout_bottom = QFormLayout()
        layout_bottom.addRow(u'结果', self._wid_result)
        layout_bottom.addRow(u'备注', self._wid_comment)

        layout_bottom.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        group_bottom = QGroupBox()
        group_bottom.setLayout(layout_bottom)

        # 布局
        layout_main = QVBoxLayout()
        layout_main.addWidget(group_top)
        layout_main.addWidget(group_bottom)
        layout_main.addStretch(1)
        layout_main.addWidget(btn_debug)

        self.setLayout(layout_main)

        self.setStyleSheet(get_theme('WebDebug'))

        btn_debug.sig_clicked.connect(self.debug)

        # 设置当前控件
        self._current_debug = self._wid_debug_page

    def set_index(self, p_index):
        """
        切换到页面高度
        :param p_index:
        :return:
        """
        self._wid_debug.setCurrentIndex(p_index)

        if 0 == p_index:
            self._current_debug = self._wid_debug_page
        elif 1 == p_index:
            self._current_debug = self._wid_debug_window
        else:
            self._current_debug = self._wid_debug_widget

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        self._current_debug.set_data(p_data)

    def debug(self):
        """
        执行调试命令
        :return:
        """

        cls_cmd = self._current_debug.get_data()

        command = OrcCmd()

        driver_command = OrcDriverCmd()
        driver_command.set_cmd(cls_cmd)

        command.set_cmd(driver_command)

        _resource = OrcSocketResource('Driver')
        _result = _resource.get(command.get_cmd_dict())

        if _result.data:
            self._set_result('PASS')
        else:
            self._set_result('FAIL')

        self._set_comment(_result.message)

    def _set_result(self, p_result):
        """
        设置结果
        :param p_result:
        :return:
        """
        self._wid_result.set_data(p_result)

    def _set_comment(self, p_comment):
        """

        :param p_comment:
        :return:
        """
        self._wid_comment.set_data(p_comment)


class PageDebug(QWidget):
    """
    页面调度
    """
    def __init__(self):

        QWidget.__init__(self)

        # 标识
        self._label = WidgetCreator.create_label(self)
        self._label.setWordWrap(True)

        # 操作
        self._operation = WidgetCreator.create_complex(parent=None, p_type='OPE_SELECT')

        # 布局
        layout_main = QFormLayout()
        layout_main.addRow(u'标识:', self._label)
        layout_main.addRow(u'操作:', self._operation)

        layout_main.setContentsMargins(0, 0, 0, 0)
        layout_main.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.setLayout(layout_main)

        self._page_def_data = None
        self._page_det_data = None

    def clear(self):
        """
        清空
        :return:
        """
        self._label.clear()
        self._operation.clear()

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        self._data = p_data

        self._page_def_data = p_data[0]
        self._page_det_data = p_data[1]

        page_flag = "%s[%s]" % (self._page_def_data['page_flag'], self._page_det_data['test_env'])

        self._label.set_data(page_flag)

        self._operation.set_sense('DEBUG')
        self._operation.set_type('PAGE')

    def get_data(self):
        """
        获取界面数据
        :return:
        :rtype: OrcWebCmd
        """
        res_cmd = WebCmd()
        res_cmd.set_cmd_type(WebObjectType.PAGE)
        res_cmd.set_cmd_object(self._page_def_data['id'])
        res_cmd.set_cmd_operation(self._operation.get_data())

        return res_cmd


class WindowDebug(QWidget):
    """
    窗口调试
    """
    def __init__(self):

        QWidget.__init__(self)

    def clear(self):
        """
        清空
        :return:
        """
        pass

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        pass

    def get_data(self):
        """
        获取界面数据
        :return:
        """
        pass


class WidgetDebug(QWidget):
    """
    控件调度
    """
    def __init__(self):

        QWidget.__init__(self)

        # 标识
        self._label = WidgetCreator.create_label(self)

        # 控件类型
        self._type = WidgetCreator.create_complex(parent=self, p_type='TYPE_SELECT')
        self._type.setEnabled(False)

        # 操作
        self._operation = WidgetCreator.create_complex(parent=self, p_type='OPE_SELECT')

        # 数据
        self._data = WidgetCreator.create_line_text()

        # 布局
        layout_main = QFormLayout()
        layout_main.addRow(u'标识:', self._label)
        layout_main.addRow(u'类型:', self._type)
        layout_main.addRow(u'操作:', self._operation)
        layout_main.addRow(u'数据:', self._data)

        layout_main.setContentsMargins(0, 0, 0, 0)
        layout_main.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.setLayout(layout_main)

        self._widget_data = None

    def clear(self):
        """
        清空
        :return:
        """
        self._label.clear()
        self._type.clear()
        self._operation.clear()
        self._data.clear()

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        self._widget_data = p_data

        flag_data = self._widget_data['widget_path']

        data_len = len(flag_data) / 20
        data_len = data_len if len(flag_data) % 20 == 0 else data_len + 1
        data = '<br>'.join([flag_data[frg * 20:(frg + 1) * 20] for frg in range(data_len)])

        self._label.set_data(data)
        self._type.set_data(self._widget_data['widget_type'])
        self._operation.set_type(self._widget_data['widget_type'])

    def get_data(self):
        """
        获取界面数据
        :return:
        """
        res_cmd = WebCmd()
        res_cmd.set_cmd_type(WebObjectType.WIDGET)
        res_cmd.set_cmd_object(self._widget_data['id'])
        res_cmd.set_cmd_operation(self._operation.get_data())
        res_cmd.set_data(self._data.get_data())

        return res_cmd
