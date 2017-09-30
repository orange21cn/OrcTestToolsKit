# coding=utf-8
import os
import json
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QWidget
from PySide.QtGui import QPushButton
from PySide.QtGui import QSizePolicy
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QComboBox
from PySide.QtGui import QLineEdit
from PySide.QtGui import QTextEdit
from PySide.QtGui import QFileDialog
from PySide.QtGui import QProgressBar
from PySide.QtGui import QIcon

from OrcLib import get_config
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibTheme import OrcTheme


class WidgetCreator(object):

    _configer = get_config()

    def __init__(self):

        object.__init__(self)

    @staticmethod
    def create_label(parent=None):
        """

        :param p_text:
        :param parent:
        :return:
        """
        return OrcLabel(parent=parent)

    @staticmethod
    def create_line_text(parent=None):
        """
        创建单行输入控件
        :param parent:
        :return:
        """
        return OrcLineEdit(parent)

    @staticmethod
    def create_text_area(parent=None):
        """
        创建多行输入控件
        :param parent:
        :return:
        """
        return OrcTextArea(parent)

    @staticmethod
    def create_select(flag, empty=False, parent=None):
        """
        创建下拉框
        :param parent:
        :param empty:
        :param flag:
        :return:
        """
        return OrcSelect(parent, flag, empty)

    @staticmethod
    def create_process(steps, parent=None):
        """

        :param steps:
        :param parent:
        :return:
        """
        return OrcProcess(parent, steps)

    @staticmethod
    def create_display(parent=None):
        """

        :param parent:
        :return:
        """
        return OrcDisplay(parent)

    @staticmethod
    def create_file_selection(parent=None):
        """

        :param parent:
        :return:
        """
        return OrcFileSelection(parent)

    @staticmethod
    def create_pagination(parent=None):
        """

        :param parent:
        :return:
        """
        return OrcPagination(parent)

    @classmethod
    def create_complex(cls, parent, p_type, *args, **kwargs):
        """
        创建自定义复杂控件,控件在文件中定义,动态导入
        :param parent:
        :param kwargs:
        :param args:
        :param p_type:
        :return:
        """
        view_home = cls._configer.get_option('VIEWLIB', 'path')
        view_conf_file = os.path.join(view_home, "views.path")

        with open(view_conf_file, 'r') as conf_file:
            view_conf = json.loads(conf_file.read())

        widget_path = view_conf[p_type]['PATH']
        widget_name = view_conf[p_type]['NAME']

        if p_type not in view_conf:
            return None
        print args, kwargs
        return getattr(__import__(widget_path, fromlist=True), widget_name)(parent)

    @staticmethod
    def create_widget(parent, p_def):
        """
        创建界面用控件,同一类型会根据不同的使用环境有所不同
        :param parent:
        :param p_def: 控件定义 {TYPE, SOURCE, FLAG}
        :return:
        """
        creator = WidgetCreator()

        # 参数判断
        if not isinstance(p_def, dict):
            return

        widget_type = None if 'TYPE' not in p_def else p_def['TYPE']
        widget_source = None if 'SOURCE' not in p_def else p_def['SOURCE']
        widget_flag = None if 'FLAG' not in p_def else p_def['FLAG']

        # 单行输入框
        if 'LINETEXT' == widget_type:
            return OrcLineEdit(parent)

        # 多行输入框
        elif 'TEXTAREA' == widget_type:

            if 'SEARCH' == widget_source:
                return OrcLineEdit(parent)
            else:
                return OrcTextArea(parent)

        # 时间显示
        elif 'DATETIME' == widget_type:
            return OrcLineEdit(parent)

        # display
        elif 'DISPLAY' == widget_type:
            return OrcDisplay(parent)

        # 选择输入框
        elif 'SELECT' == widget_type:

            if 'SEARCH' == widget_source:
                return OrcSelect(parent, widget_flag, True)
            else:
                return OrcSelect(parent, widget_flag)

        # 其他
        else:
            return creator.create_complex(parent, widget_type, widget_flag, widget_source)


class OrcLabel(QLabel):

    def __init__(self, p_text=None, parent=None):

        super(OrcLabel, self).__init__(parent)

        if p_text is not None:
            self.set_data(p_text)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def set_data(self, p_data):
        self.setText(p_data)

    def get_data(self):
        return self.text()


class OrcLineEdit(QLineEdit):
    """
    单行输入框
    """
    clicked = OrcSignal()

    def __init__(self, parent=None):

        super(OrcLineEdit, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def get_data(self):
        """
        获取数据
        :return:
        """
        return self.text()

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        return self.setText(p_data)

    def mousePressEvent(self, *args, **kwargs):
        """
        鼠标点击事件
        :param args:
        :param kwargs:
        :return:
        """
        self.clicked.emit()


class OrcDisplay(QLineEdit):
    """
    单行显示框,值和显示内容不一样
    """
    clicked = OrcSignal()

    def __init__(self, parent=None):

        super(OrcDisplay, self).__init__(parent)

        self.text = None
        self.value = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setReadOnly(True)

    def get_data(self):
        """
        获取数据,只获取 text
        :return:
        """
        return self.value

    def set_data(self, p_data):
        """
        设置同时设置 text/value
        :param p_data: (value, text)
        :return:
        """
        self.value = p_data[0]
        self.text = p_data[1]

        return self.setText(self.text)

    def mousePressEvent(self, *args, **kwargs):
        """
        鼠标点击事件
        :param args:
        :param kwargs:
        :return:
        """
        self.clicked.emit()


class OrcTextArea(QTextEdit):
    """
    多行输入框
    """
    clicked = OrcSignal()

    def __init__(self, parent=None):

        super(OrcTextArea, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def mousePressEvent(self, *args, **kwargs):
        """
        鼠标点击事件
        :param args:
        :param kwargs:
        :return:
        """
        self.clicked.emit()

    def get_data(self):
        """
        获取数据
        :return:
        """
        return self.toPlainText()

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        self.setText(p_data)


class OrcFileSelection(QWidget):
    """
    文件选择控件
    """
    def __init__(self, parent=None):

        super(OrcFileSelection, self).__init__(parent)

        # 文件名显示框
        self._file_name = OrcLineEdit()

        # 文件选择按钮
        self._file_btn = QPushButton('...')

        # 布局
        layout_main = QHBoxLayout()
        layout_main.addWidget(self._file_name)
        layout_main.addWidget(self._file_btn)

        layout_main.setContentsMargins(0, 0, 0, 0)
        layout_main.setSpacing(0)

        self.setLayout(layout_main)

        self._file_btn.clicked.connect(self.__select_file)

    def mousePressEvent(self, *args, **kwargs):
        """
        鼠标点击事件
        :param args:
        :param kwargs:
        :return:
        """
        self.clicked.emit()

    def __select_file(self):
        """
        选择文件
        :return:
        """
        directory_name = QFileDialog.getExistingDirectory(self, u'选择')
        self._file_name.set_data(directory_name)


class OrcSelectBase(QComboBox):
    """
    下拉列表基础类
    """
    # 增加 clicked 保持与其他控件一致,但不修改属性避免与点击下拉冲突
    clicked = OrcSignal()

    def __init__(self, parent=None, empty=False):
        """
        User defined combobox, it's data is come from table lib_dictionary
        :param empty: 是否包含空数据
        :return:
        """
        super(OrcSelectBase, self).__init__(parent)

        # 显示文字集
        self._texts = []

        # 属性名称集
        self._names = []

        # 是否包含空选项
        self._empty = empty

        # 设置在拉伸方式
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # 设置样式
        self.setStyleSheet(get_theme("Input"))

    def _set_item_data(self, p_data=None):
        """
        设置 item
        :param p_data:
        :return:
        """
        self.clear()
        self._texts = []
        self._names = []

        if p_data is None:
            return

        # 新建时先清空
        self.clear()

        # 可为空时加空数据
        if self._empty:
            self.addItem("", "")
            self._texts.append("")
            self._names.append("")

        # 加入 item
        for _item in p_data:
            self.addItem(_item["text"], _item["name"])
            self._names.append(_item["name"])
            self._texts.append(_item["text"])

    def get_data(self):
        """
        获取属性数据
        :return:
        """
        return self.itemData(self.currentIndex())

    def get_text(self):
        """
        获取显示文字
        :return:
        """
        return self.itemText(self.currentIndex())

    def set_data(self, p_data):
        """
        通过属性或显示文字设置数据
        :param p_data:
        :return:
        """
        if p_data in self._texts:
            self.setCurrentIndex(self._texts.index(p_data))
        elif p_data in self._names:
            self.setCurrentIndex(self._names.index(p_data))
        else:
            pass


class OrcSelect(OrcSelectBase):
    """
    字典下拉列表
    """
    def __init__(self, parent=None, flag=None, empty=False):

        super(OrcSelect, self).__init__(parent, empty)

        self.__resource = OrcResource('Dict')

        if flag is not None:
            self.set_flag(flag)

    def set_flag(self, p_flag):
        """
        设置下拉选项
        :param p_flag:
        :return:
        """
        self.clear()

        result = self.__resource.get(
            parameter=dict(TYPE='dictionary', DATA=dict(dict_flag=p_flag)))

        if not ResourceCheck.result_status(result, u'获取字典信息'):
            dict_result = list()
        else:
            dict_result = result.data

        dict_data = [dict(name=_item['dict_value'], text=_item['dict_text'])
                     for _item in dict_result]

        self._set_item_data(dict_data)


class OrcProcess(QProgressBar):
    """
    进度条
    """
    sig_finish = OrcSignal()

    def __init__(self, parent=None, steps=None):

        super(QProgressBar, self).__init__(parent)

        self.__steps = 1 if steps is None else steps
        self.__length = 100 / self.__steps
        self.__value = 0

        self.setValue(0)

    def set_steps(self, p_steps):

        if 0 >= p_steps:
            return

        self.__steps = p_steps

        self.__length = 100 / self.__steps
        self.__value = 0

        self.setValue(0)

    def step_forward(self):

        self.__value += self.__length

        if 100 - self.__value <= self.__length:
            self.__value = 100

        self.setValue(self.__value)

        if 100 == self.__value:
            self.sig_finish.emit()

    def get_process(self):
        """
        获取进度
        :return:
        """
        return self.__value


class OrcPagination(QWidget):
    """
    分页类
    """
    sig_page = OrcSignal(tuple)

    def __init__(self, parent=None):

        super(OrcPagination, self).__init__(self)

        self._message = QLabel()

        self._btn_first = QPushButton()
        self._btn_first.setIcon(QIcon(OrcTheme.get_icon('previous')))

        self._btn_last = QPushButton()
        self._btn_last.setIcon(QIcon(OrcTheme.get_icon('next')))

        self._btn_previous = QPushButton()
        self._btn_previous.setIcon(QIcon(OrcTheme.get_icon('rewind')))

        self._btn_next = QPushButton()
        self._btn_next.setIcon(QIcon(OrcTheme.get_icon('forward')))

        self._jump = QComboBox()
        self._number = QLineEdit()

        layout_main = QHBoxLayout()
        layout_main.addWidget(self._message)
        layout_main.addWidget(self._btn_first)
        layout_main.addWidget(self._btn_previous)
        layout_main.addWidget(self._btn_next)
        layout_main.addWidget(self._btn_last)
        layout_main.addWidget(self._jump)
        layout_main.addWidget(self._number)

        layout_main.setContentsMargins(0, 0, 0, 0)
        layout_main.setSpacing(0)

        self.setLayout(layout_main)

        self._btn_first.clicked.connect(self.first_page)
        self._btn_last.clicked.connect(self.last_page)
        self._btn_previous.clicked.connect(self.previous_page)
        self._btn_next.clicked.connect(self.next_page)
        self._jump.currentIndexChanged.connect(self.jump_to_page)

        self.setStyleSheet(OrcTheme.get_theme('Pagination'))

        # 总页数
        self.__pages = 10

        #  当前页码
        self.__page = 1

        self._number.setText('20')
        self.set_data(0, 0)

    def get_page(self):
        """
        获取当前页码
        :return:
        """
        return self.__page

    def get_number(self):
        """
        获取每页条数
        :return:
        """
        return self._number.text()

    def set_data(self, p_page, p_pages):
        """
        设置页数和条数数据
        :param p_page: 当前页数
        :param p_pages: 总页数
        :return:
        """
        self._message.setText("%s/%s" % (p_page, p_pages))

        if self.__pages != p_pages:

            self.__pages = p_pages
            self._jump.clear()

            for _index in range(p_pages):
                _item = _index + 1
                self._jump.addItem(str(_item), str(_item))

    def first_page(self):
        """
        第一页
        :return:
        """
        self.__page = 1
        number = self._number.text()

        self.sig_page.emit((self.__page, number))

    def last_page(self):
        """
        最后一页
        :return:
        """
        self.__page = self.__pages
        number = self._number.text()

        self.sig_page.emit((self.__page, number))

    def previous_page(self):
        """
        上一页
        :return:
        """
        if 1 < self.__page:
            self.__page -= 1
        number = self._number.text()

        self.sig_page.emit((self.__page, number))

    def next_page(self):
        """
        下一页
        :return:
        """
        if self.__pages > self.__page:
            self.__page += 1
        number = self._number.text()

        self.sig_page.emit((self.__page, number))

    def jump_to_page(self):
        """
        跳转
        :return:
        """
        self.__page = int(self._jump.itemData(self._jump.currentIndex()))
        number = self._number.text()

        self.sig_page.emit((self.__page, number))


class OrcBoxWidget(QWidget):
    """
    layout 控件,用于某不没有 addlayout 的控件
    """
    def __init__(self, p_type=None):

        QWidget.__init__(self)

        if 'V' == p_type:
            self._layout = QVBoxLayout()
        else:
            self._layout = QHBoxLayout()

        self.setLayout(self._layout)

        self._layout.setContentsMargins(0, 0, 0, 0)

    def add_widget(self, p_widget):
        """
        增加控件
        :param p_widget:
        :return:
        """
        if isinstance(p_widget, QWidget):
            self._layout.addWidget(p_widget)
