# coding=utf-8
from functools import partial

from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QWidget
from PySide.QtGui import QDialog
from PySide.QtGui import QDockWidget
from PySide.QtGui import QBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QHBoxLayout

from OrcLib.LibType import DirType
from OrcLib.LibLog import OrcLog
from OrcView.Lib.LibSearch import ViewSearch
from OrcView.Lib.LibSearch import OrcNewButtons
from OrcView.Lib.LibView import OrcPagination

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


class OrcViewWidget(QBoxLayout):
    """
    普通界面,含查询/显示及按钮,
    """
    # 按钮信号
    sig_action = OrcSignal(str)

    # 右键信号
    sig_context = OrcSignal(str)

    class ViewDef(object):
        """
        普通界面,含查询/显示及按钮,
        """
        def __init__(self):

            object.__init__(self)

            # 字段定义
            self.widget_def = None

            # 是否有查询条
            self.search_enable = False

            # 查询条件列数
            self.search_column = 4

            # 界面布局方向
            self.direction = DirType.VERTICAL

            # 按钮定义
            self.buttons_def = None
            self.buttons_dir = DirType.HORIZON

            # 分页
            self.pagination_enable = False

            # 右键菜单定义
            self.context_def = None

    def __init__(self):

        QBoxLayout.__init__(self, QBoxLayout.TopToBottom)

        self._logger = _logger

        # 界面定义
        self.definition = self.ViewDef()

        # 查询条
        self.searcher = None

        # 显示
        self.display = None

        # 按钮
        self.buttons = None

        # 分页控件
        self.pagination = None

    def init_view(self):
        """
        初始化界面
        :return:
        """
        # 布局方向
        if self.definition.direction == DirType.HORIZON:
            self.setDirection(QBoxLayout.LeftToRight)

        # 查询框
        if self.definition.search_enable:
            self.searcher = ViewSearch(self.definition.widget_def, self.definition.search_column)
            self.addWidget(self.searcher)

        # 显示区
        if self.display is not None:
            self.addWidget(self.display)

        # button layout
        if self.definition.buttons_dir == DirType.HORIZON:
            layout_button = QHBoxLayout()
        else:
            layout_button = QVBoxLayout()

        # 分页
        if self.definition.pagination_enable:
            self.pagination = OrcPagination()
            layout_button.addWidget(self.pagination)
            self.pagination.sig_search.connect(partial(self.sig_action.emit, 'act_search'))

        # 按钮
        if self.definition.buttons_def is not None:
            self.buttons = OrcNewButtons(self.definition.buttons_def, self.definition.buttons_dir)
            layout_button.addStretch()
            layout_button.addWidget(self.buttons)
            self.addLayout(layout_button)
            self.buttons.sig_clicked.connect(self.sig_action)

        # 右键菜单
        if self.definition.context_def is not None:
            self.display.create_context_menu(self.definition.context_def)
            self.display.sig_context.connect(self.sig_context)

    def basic_search(self, p_callback, p_cond=None):
        """
        基本查询,含生成条件及查询
        :param p_cond: 附加查询条件
        :param p_callback: 外部查询条件
        :return:
        """
        page = 1
        number = 10
        condition = dict()

        # 有查询条
        if self.definition.search_enable:
            condition = self.searcher.get_cond()

        # 合并外部查询条件
        if isinstance(p_cond, dict):
            condition.update(p_cond)

        # 有分页条
        if self.definition.pagination_enable:

            page = self.pagination.get_page()
            number = int(self.pagination.get_number())

            if not page:
                page = 1
            else:
                page = int(page)

            condition = dict(page=page, number=number, condition=condition)

        # 查询
        p_callback(condition)

        # 更新分页栏数据
        if self.definition.pagination_enable:

            number = 1 if number < 1 else number
            record_num = int(self.display.model.mod_get_record_num())

            self.pagination.set_data(page, record_num / number)


class OrcDisplayView(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self._logger = _logger

        # 控件
        self.main = OrcViewWidget()
        self.setLayout(self.main)

        # +---- Connection ----+
        # 点击按钮
        self.main.sig_action.connect(self._dispatch_action)

        # 右键菜单
        self.main.sig_context.connect(self._dispatch_context)

    def _dispatch_action(self, p_flag):
        """
        点击按钮后操作
        :param p_flag:
        :return:
        """
        try:
            getattr(self, "%s" % p_flag)()
        except AttributeError:
            self._logger.error("Button clicked but no func founded")

    def _dispatch_context(self, p_flag):
        """
        右键菜单操作
        :param p_flag:
        :return:
        """
        try:
            getattr(self, "%s" % p_flag)()
        except AttributeError:
            self._logger.error("Right clicked but no func founded")


class OrcDialogView(QDialog):

    def __init__(self):

        QDialog.__init__(self)

        self._logger = _logger

        # 控件
        self.main = OrcViewWidget()
        self.setLayout(self.main)

        # 初始化控件
        self.main.init_view()

        # +---- Connection ----+
        # 点击按钮
        self.main.sig_action.connect(self._dispatch_action)

        # 右键菜单
        self.main.sig_context.connect(self._dispatch_context)

        # 数据,用于保存返回数据
        self._data = None

    def _dispatch_action(self, p_flag):
        """
        点击按钮后操作
        :param p_flag:
        :return:
        """
        try:
            getattr(self, "%s" % p_flag)()
        except AttributeError:
            self._logger.error("Button clicked but no func founded")

    def _dispatch_context(self, p_flag):
        """
        右键菜单操作
        :param p_flag:
        :return:
        """
        try:
            getattr(self, "%s" % p_flag)()
        except AttributeError:
            self._logger.error("Right clicked but no func founded")

    def act_submit(self):
        """
        提交
        :return:
        """
        pass

    def act_cancel(self):
        """
        取消
        :return:
        """
        self.close()
