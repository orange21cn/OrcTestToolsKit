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
from OrcLib.LibException import OrcPostFailedException
from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTheme import get_theme
from OrcView.Lib.LibTheme import OrcTheme

_logger = LogClient()


class WidgetFactory(object):

    _configer = get_config()

    def __init__(self):

        object.__init__(self)

    @staticmethod
    def create_line_text():
        """
        创建单行输入控件
        :return:
        """
        return OrcLineEdit()

    @staticmethod
    def create_text_area():
        """
        创建多行输入控件
        :return:
        """
        return OrcTextArea()

    @staticmethod
    def create_select(p_flag, p_empty=False):
        """
        创建下拉框
        :param p_empty:
        :param p_flag:
        :return:
        """
        return OrcSelect(p_flag, p_empty)

    @staticmethod
    def create_basic(p_type, p_flag=None, p_source=None):
        """
        创建基本控件
        :param p_flag: 标识,用于创建下拉框
        :param p_source: 使用的场景,有时候显示和查询会有不同
        :param p_type: 控件类型
        :return:
        """
        _type = p_type
        _source = p_source
        _flag = '' if p_flag is None else p_flag

        # 单行输入框
        if 'LINETEXT' == _type:
            return OrcLineEdit()

        # 多行输入框
        elif 'TEXTAREA' == _type:

            if 'SEARCH' == _source:
                return OrcLineEdit()
            else:
                return OrcTextArea()

        # 时间显示
        elif 'DATETIME' == _type:
            return OrcLineEdit()

        # 时间显示
        elif 'DISPLAY' == _type:
            return OrcDisplay()

        # 选择输入框
        elif 'SELECT' == _type:

            if 'SEARCH' == _source:
                return OrcSelect(_flag, True)
            else:
                return OrcSelect(_flag)

        # 选择控件操作类型
        elif 'SEL_WIDGET' == _type:
            _view = OrcSelectWidgetType()
            if 'SEARCH' == _source:
                # Todo 增加一个公共函数
                _view.insertItem(0, u'所有', '')
            _view.setCurrentIndex(0)
            return _view

        # 操作类型
        elif 'OPERATE' == _type:
            return OrcOperate()

        # 其他
        else:
            return OrcLineEdit()

    @classmethod
    def create_complex(cls, p_type, p_flag=None, p_source=None):
        """
        创建自定义复杂控件,控件在文件中定义,动态导入
        :param p_flag:
        :param p_source:
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

        return getattr(__import__(widget_path, fromlist=True), widget_name)()

    @staticmethod
    def create_widget(p_def):
        """
        创建界面用控件,同一类型会根据不同的使用环境有所不同
        :param p_def:
        :return:
        """
        creator = WidgetFactory()

        widget_type = ''
        widget_source = ''
        widget_flag = ''

        # 参数判断
        if isinstance(p_def, str):
            widget_type = p_def
        elif isinstance(p_def, dict):
            if 'TYPE' in p_def:
                widget_type = p_def['TYPE']
            if 'SOURCE' in p_def:
                widget_source = p_def['SOURCE']
            if 'FLAG' in p_def:
                widget_flag = p_def['FLAG']
        else:
            pass

        if widget_type in ('LINETEXT', 'TEXTAREA', 'DATETIME', 'DISPLAY',
                           'SELECT', 'SEL_WIDGET', 'OPERATE'):
            return creator.create_basic(widget_type, widget_flag, widget_source)
        else:
            return creator.create_complex(widget_type, widget_flag, widget_source)


class OrcLineEdit(QLineEdit):
    """
    单行输入框
    """
    clicked = OrcSignal()

    def __init__(self):
        QLineEdit.__init__(self)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def get_data(self):
        return self.text()

    def set_data(self, p_data):
        return self.setText(p_data)

    def mousePressEvent(self, *args, **kwargs):
        self.clicked.emit()


class OrcDisplay(QLineEdit):
    """
    单行输入框
    """
    clicked = OrcSignal()

    def __init__(self):
        QLineEdit.__init__(self)

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
        self.clicked.emit()


class OrcTextArea(QTextEdit):
    """
    多行输入框
    """
    clicked = OrcSignal()

    def __init__(self):
        QTextEdit.__init__(self)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def mousePressEvent(self, *args, **kwargs):
        self.clicked.emit()

    def get_data(self):
        return self.toPlainText()

    def set_data(self, p_data):
        self.setText(p_data)


class OrcFileSelection(QWidget):
    """
    文件选择控件
    """
    def __init__(self):

        QWidget.__init__(self)

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

    def __select_file(self):
        """
        选择文件
        :return:
        """
        directory_name = QFileDialog.getExistingDirectory(self, u'选择')
        self._file_name.set_data(directory_name)


class OrcOperate(QLineEdit):
    """
    ToBeDeleted
    """
    sig_operate = OrcSignal()
    clicked = OrcSignal()

    def __init__(self):

        QLineEdit.__init__(self)

        self.__data = None

        self.setReadOnly(True)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    def get_data(self):
        return self.__data

    def set_data(self, p_data):
        self.__data = p_data
        _text = operate_to_str(p_data)
        return self.setText(_text)

    def mousePressEvent(self, *args, **kwargs):
        self.sig_operate.emit()


class OrcSelectBase(QComboBox):
    """
    下拉列表基础类
    """
    # 增加 clicked 保持与其他控件一致,但不修改属性避免与点击下拉冲突
    clicked = OrcSignal()

    def __init__(self, p_empty=False):
        """
        User defined combobox, it's data is come from table lib_dictionary
        :param p_empty: 是否包含空数据
        :return:
        """
        QComboBox.__init__(self)

        # 显示文字集
        self.__texts = []

        # 属性名称集
        self.__names = []

        # 是否包含空选项
        self.empty = p_empty

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
        self.__texts = []
        self.__names = []

        if p_data is None:
            return

        # 新建时先清空
        self.clear()

        # 可为空时加空数据
        if self.empty:
            self.addItem("", "")
            self.__texts.append("")
            self.__names.append("")

        # 加入 item
        for _item in p_data:
            self.addItem(_item["text"], _item["name"])
            self.__names.append(_item["name"])
            self.__texts.append(_item["text"])

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
        print "==-->>", p_data
        print self.__names
        if p_data in self.__texts:
            self.setCurrentIndex(self.__texts.index(p_data))
        elif p_data in self.__names:
            self.setCurrentIndex(self.__names.index(p_data))
        else:
            pass


class OrcSelect(OrcSelectBase):
    """
    字典下拉列表
    """
    def __init__(self, p_type=None, p_empty=False):

        OrcSelectBase.__init__(self, p_empty)

        self.__resource = OrcResource('Dict')

        if p_type is not None:
            self.set_type(p_type)

    def set_type(self, p_type):
        """
        设置下拉选项
        :param p_type:
        :return:
        """
        self.clear()

        result = self.__resource.get(
            parameter=dict(TYPE='dictionary', DATA=dict(dict_flag=p_type)))

        if not ResourceCheck.result_status(result, u'获取字典信息'):
            dict_result = list()
        else:
            dict_result = result.data

        dict_data = [dict(name=_item['dict_value'], text=_item['dict_text'])
                     for _item in dict_result]

        self._set_item_data(dict_data)


class OrcSelectWidgetType(OrcSelectBase):
    """
    下拉控件类型列表
    """
    def __init__(self, p_empty=False):
        """
        User defined combobox, it's data is come from table lib_dictionary
        :param p_empty: 是否包含空数据
        :return:
        """
        OrcSelectBase.__init__(self, p_empty)

        self.__resource = OrcResource('Dict')

        result = self.__resource.get(
            parameter=dict(TYPE='widget_type', DATA=dict()))

        if not ResourceCheck.result_status(result, u'获取字典信息'):
            dict_result = list()
        else:
            dict_result = result.data

        _data = [dict(name=_item['type_name'], text=_item['type_text'])
                 for _item in dict_result]

        self._set_item_data(_data)


class OrcSelectWidgetOperation(OrcSelectBase):
    """
    下拉控件类型列表
    """
    def __init__(self, p_type=None, p_empty=False):
        """
        User defined combobox, it's data is come from table lib_dictionary
        :param p_empty: 是否包含空值
        :return:
        """
        OrcSelectBase.__init__(self, p_empty)

        self.__resource = OrcResource('Dict')

        if p_type is not None:
            self.set_type(p_type)

    def set_type(self, p_type):

        self.clear()

        result = self.__resource.get(
            parameter=dict(TYPE='widget_operation', DATA=dict(type_name=p_type)))

        if not ResourceCheck.result_status(result, u'获取控件操作信息'):
            dict_result = list()
        else:
            dict_result = result.data

        # 获取当前控件的操作方式,去除不可操作控件
        if p_type in ("WINDOW", "GROUP"):
            return

        _data = [dict(name=_item['ope_name'], text=_item['ope_text'])
                 for _item in dict_result]

        # 获取基本操作方式
        if p_type not in ("PAGE", "BLOCK"):

            result = self.__resource.get(
                parameter=dict(TYPE='widget_operation', DATA=dict(type_name='BLOCK')))

            if ResourceCheck.result_status(result, u'获取基本控件操作信息'):
                _data.extend([dict(name=_item['ope_name'], text=_item['ope_text']) for _item in result.data])

        self._set_item_data(_data)


def operate_to_str(p_data):
    """
    :param p_data: {'OBJECT': '3200000002', 'OPERATE': u'INPUT', 'TYPE': u'WIDGET'}
    :return:
    """
    if not isinstance(p_data, dict):
        return p_data

    resource_dict = OrcResource("Dict")

    def get_widget_def_path(p_id):
        """
        获取控件路径
        :param p_id:
        :return:
        """
        resource_widget_def = OrcResource("WidgetDef")
        result = resource_widget_def.get(path=p_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取控件路径"):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u"获取控件路径")

        return result.data["widget_path"]

    def get_page_def_flag(p_id):
        """
        获取页面标识
        :param p_id:
        :return:
        """
        resource_page_def = OrcResource("PageDef")
        result = resource_page_def.get(path=p_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取页面标识"):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u"获取页面标识")

        return result.data["page_flag"]

    def get_lib_dict_text(p_flag, p_value):
        """
        获取操作文字
        :param p_value:
        :param p_flag:
        :return:
        """
        result = resource_dict.get(parameter=dict(dict_flag=p_flag, dict_value=p_value))

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取操作文字"):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u"获取操作文字")

        return result.data[0]["dict_text"]

    _type = p_data["TYPE"]
    _object = p_data["OBJECT"]

    if "WIDGET" == _type:

        _operation = p_data["OPERATION"]

        try:
            _object = get_widget_def_path(_object)
            _type = get_lib_dict_text("operate_object_type", _type)

            result = resource_dict.get(
                parameter=dict(TYPE='widget_operation', DATA=dict(ope_name=_operation)))

            # 检查结果
            if not ResourceCheck.result_status(result, u"获取操作类型文字"):
                return ""

            _operation = result.data[0]['ope_text']

        except OrcPostFailedException:
            # Todo
            pass

        return "%s->%s->%s" % (_operation, _type, _object)

    else:
        try:
            _object = get_page_def_flag(_object)
            _type = get_lib_dict_text("operate_object_type", _type)
        except OrcPostFailedException:
            # Todo
            pass

        return "%s->%s" % (_type, _object)


class ObjectOperator(QVBoxLayout):
    """

    """
    def __init__(self):

        QVBoxLayout.__init__(self)

        _label_type = QLabel(u"对象类型:")
        self.__type = OrcSelectWidgetType()

        _layout_type = QHBoxLayout()
        _layout_type.addWidget(_label_type)
        _layout_type.addWidget(self.__type)

        _label_operate = QLabel(u"操作方式:")
        self.__operate = OrcSelectWidgetOperation()

        _layout_operate = QHBoxLayout()
        _layout_operate.addWidget(_label_operate)
        _layout_operate.addWidget(self.__operate)

        self.addLayout(_layout_type)
        self.addLayout(_layout_operate)

        self.__set_type()

        self.__type.currentIndexChanged.connect(self.__set_type)

    def __set_type(self):

        _type = self.__type.get_data()

        if "WIDGET" == _type:
            self.__operate.set_type(_type)
        elif "PAGE" == _type:
            self.__operate.set_type("page_operator")
        else:
            self.__operate.set_type("")

    def get_data(self):

        _data = {"TYPE": self.__type.get_data()}

        if self.__operate.get_data() is not None:
            _data["OPERATE"] = self.__operate.get_data()

        return _data


class OrcProcess(QProgressBar):
    """
    进度条
    """
    sig_finish = OrcSignal()

    def __init__(self, p_steps=None):

        QProgressBar.__init__(self)

        self.__steps = 1 if p_steps is None else p_steps
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

    def __init__(self):

        QWidget.__init__(self)

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


class OrcRow(QHBoxLayout):
    """
    模拟 FromLayout 的row
    """
    clicked = OrcSignal()

    def __init__(self, p_label, p_widget):

        QHBoxLayout.__init__(self)

        label = QLabel(p_label)

        self._widget = p_widget

        self.addWidget(label)
        self.addWidget(self._widget)

        self._widget.clicked.connect(self.clicked.emit)

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        try:
            func = getattr(self._widget, 'set_data')
            func(p_data)
        except AttributeError:
            _logger.error("widget has no func set_data")

    def get_data(self):
        """
        获取数据
        :return:
        """
        try:
            func = getattr(self._widget, 'get_data')
            return func()
        except AttributeError:
            _logger.error("widget has no func get_widget")
