# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QDialog
from PySide.QtGui import QDockWidget
from PySide.QtGui import QVBoxLayout

from OrcLib.LibLog import OrcLog

from OrcLib.LibLog import OrcLog
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import OrcButtons

_logger = OrcLog('basic.view.lib.shell')


class DockerCreator(QDockWidget):
    """
    Docker 壳
    """
    def __init__(self):

        QDockWidget.__init__(self)

        # self.setWindowTitle("Debug")
        # self.setWidget(WebDebug())
        #
        # self.setStyleSheet(get_theme('DockRight'))


class ViewWithSearch(QWidget):
    """
    界面带有查询
    """
    def __init__(self):

        QWidget.__init__(self)

        self._logger = OrcLog('basic.shell.view_with_search')

        # 控件定义
        self._def = None

        # 输入控件
        self._widget = None

        # 查询控件
        self._searcher = None

        # 左键菜单定义
        self._context_def = None

    def init_view(self, p_widget):
        """
        初始化界面
        :param p_widget:
        :return:
        """
        # 查询控件
        if self._def is not None:
            self._searcher = ViewSearch(self._def)

        # 右键菜单
        if self._context_def is not None:
            try:
                self._widget.create_context_menu(self._context_def)
            except AttributeError:
                self._logger.error('Widget has now method named create_context_menu')

        # 布局
        layout_main = QVBoxLayout()

        if self._searcher is not None:
            layout_main.addWidget(self._searcher)

        if self._widget is not None:
            layout_main.addWidget(self._widget)

        self.setLayout(layout_main)


class ViewWithButton(QWidget):
    """
    界面带有底部 button
    """
    def __init__(self):

        QWidget.__init__(self)

    def init_view(self, p_widget, p_button_def):
        """
        初始化控件
        :param p_widget:
        :param p_button_def:
        :return:
        """


class ViewWithSearchAndButton(QWidget):

    def __init__(self):

        QWidget.__init__(self)

    # def init_view(self, p_widget, p_buttons):


class OrcBasicView(QWidget):
    """
    普通界面,含查询/显示及按钮,
    """
    def __init__(self):

        QWidget.__init__(self)

        self._logger = _logger

        # 字段定义
        self._def = None

        # 是否有查询条
        self._searcher_enable = False

        # 查询条
        self.searcher = None

        # 显示
        self.display = None

        # 按钮定义
        self._buttons_def = None

        # 按钮
        self.buttons = None

        # 右键菜单定义
        self._context_def = None

        # layout
        self._layout_main = QVBoxLayout()
        self.setLayout(self._layout_main)

        # 样式
        self.setContentsMargins(0, 0, 0, 0)

        # +---- Connection ----+

    def init_view(self):
        """
        初始化界面
        :return:
        """
        # 查询框
        if self._searcher_enable:
            self.searcher = ViewSearch(self._def)
            self._layout_main.addWidget(self.searcher)

        # 显示区
        if self.display is not None:
            self._layout_main.addWidget(self.display)

        # 按钮
        if self._buttons_def is not None:
            self.buttons = OrcButtons(self._buttons_def)
            self._layout_main.addWidget(self.buttons)
            self.buttons.sig_clicked.connect(self._operate)

        # 右键菜单
        if self._context_def is not None:
            self.display.create_context_menu(self._context_def)
            self.display.sig_context.connect(self._context)

    def _operate(self, p_flag):
        """
        点击按钮后操作
        :param p_flag:
        :return:
        """
        pass

    def _context(self, p_flag):
        """
        右键菜单操作
        :param p_flag:
        :return:
        """
        pass


class OrcBasicSelector(QDialog):
    """
    普通界面,含查询/显示及按钮,
    """
    def __init__(self):

        QDialog.__init__(self)

        self._logger = _logger

        # 字段定义
        self._def = None

        # 是否有查询条
        self._search_enable = False

        # 查询条栏数
        self._search_column = 4

        # 查询条
        self.searcher = None

        # 显示
        self.display = None

        # 按钮定义
        self._buttons_def = None

        # 按钮
        self.buttons = None

        # layout
        self._layout_main = QVBoxLayout()
        self.setLayout(self._layout_main)

        # 样式
        self.setContentsMargins(0, 0, 0, 0)

        # 数据,用于保存返回数据
        self._data = None

        # +---- Connection ----+

    def init_view(self):
        """
        初始化界面
        :return:
        """
        # 查询框
        if self._search_enable:
            self.searcher = ViewSearch(self._def, self._search_column)
            self._layout_main.addWidget(self.searcher)

        # 显示区
        if self.display is not None:
            self._layout_main.addWidget(self.display)

        # 按钮
        if self._buttons_def is None:
            self._buttons_def = [dict(id="submit", name=u"确定"), dict(id="cancel", name=u"取消")]

        self.buttons = OrcButtons(self._buttons_def)

        self._layout_main.addWidget(self.buttons)
        self.buttons.sig_clicked.connect(self._operate)

    def _operate(self, p_flag):
        """
        点击按钮后操作
        :param p_flag:
        :return:
        """
        if 'submit' == p_flag:
            self._data = self.display.get_data()
            self.close()
        elif 'cancel' == p_flag:
            self.close()
        else:
            pass
