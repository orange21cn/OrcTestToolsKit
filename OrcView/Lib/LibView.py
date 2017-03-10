# coding=utf-8
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
from PySide.QtGui import QProgressBar
from LibDict import LibDict
from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import orc_db
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibException import OrcPostFailedException
from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTheme import get_theme

_logger = LogClient()


def clean_layout(p_layout):
    """
    清空 layout, 暂时未用到
    :param p_layout:
    :return:
    """
    if p_layout is not None:

        while p_layout.count():

            t_child = p_layout.takeAt(0)
            if t_child.widget() is not None:
                t_child.widget().deleteLater()
            elif t_child.layout() is not None:
                clean_layout(t_child.layout())


def create_editor(parent, p_type):
    """
    :param parent:
    :param p_type: {"TYPE": "LINETEXT",
                    "SOURCE": "SEARCH",
                    "FLAG": "CASE_DEF:CASE_TYPE"}
    :return:
    """
    # 单行输入框
    if "LINETEXT" == p_type["TYPE"]:
        return OrcLineEdit()

    # 多行输入框
    elif "TEXTAREA" == p_type["TYPE"]:
        if "SEARCH" == p_type["SOURCE"]:
            return OrcLineEdit()
        else:
            return OrcTextArea(parent)

    # 时间显示
    elif "DATETIME" == p_type["TYPE"]:
        return OrcLineEdit()

    # 时间显示
    elif "DISPLAY" == p_type["TYPE"]:
        return OrcDisplay()

    # 选择输入框
    elif "SELECT" == p_type["TYPE"]:
        _view = OrcSelect(p_type["FLAG"])
        if "SEARCH" == p_type["SOURCE"]:
            _view.insertItem(0, u"所有", "")
        _view.setCurrentIndex(0)
        return _view

    # 选择控件操作类型
    elif "SEL_WIDGET" == p_type["TYPE"]:
        _view = SelectWidgetType()
        if "SEARCH" == p_type["SOURCE"]:
            _view.insertItem(0, u"所有", "")
        _view.setCurrentIndex(0)
        return _view

    # 其他
    elif "OPERATE" == p_type["TYPE"]:
        return OrcOperate(parent)

    # 其他
    else:
        return OrcLineEdit()


def get_dict(p_flag):
    """
    获取下拉框定义
    :param p_flag: 标识,使用字段名定义,特殊的使用字段名和属性名
    :return:
    """
    _items = orc_db.session. \
        query(LibDictionary). \
        filter(LibDictionary.dict_flag == p_flag). \
        order_by(LibDictionary.dict_order)

    return _items


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

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def mousePressEvent(self, *args, **kwargs):
        self.clicked.emit()

    def get_data(self):
        return self.toPlainText()

    def set_data(self, p_data):
        self.setText(p_data)


class OrcOperate(QLineEdit):
    sig_operate = OrcSignal()
    clicked = OrcSignal()

    def __init__(self, parent):
        QLineEdit.__init__(self, parent)

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


class OrcSelect(QComboBox):
    """
    下拉列表, 将被替换
    """
    # 增加 clicked 保持与其他控件一致,但不修改属性避免与点击下拉冲突
    clicked = OrcSignal()

    def __init__(self, p_flag=None):
        """
        User defined combobox, it's data is come from table lib_dictionary
        :param p_flag: 数据库中的标识符
        :return:
        """
        QComboBox.__init__(self)

        self.__empty = False
        self.__text = []
        self.__value = []

        if p_flag is not None:
            self.set_flag(p_flag)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    # def mousePressEvent(self, *args, **kwargs):
    #     self.clicked.emit()

    def set_flag(self, p_flag):

        self.__text = []
        self.__value = []
        self.clear()

        # Todo
        _items = orc_db.session. \
            query(LibDictionary). \
            filter(LibDictionary.dict_flag == p_flag). \
            order_by(LibDictionary.dict_order).all()

        if self.__empty:
            _items[0:0] = [LibDictionary(dict(
                id=0,
                dict_flag="",
                dict_text="",
                dict_order=0,
                dict_value="",
                dict_desc=""
            ))]

        for t_item in _items:
            self.addItem(t_item.dict_text, t_item.dict_value)
            self.__text.append(t_item.dict_text)
            self.__value.append(t_item.dict_value)

    def set_empty(self):
        self.__empty = True

    def get_data(self):
        return self.itemData(self.currentIndex())

    def get_text(self):
        return self.itemText(self.currentIndex())

    def set_data(self, p_data):

        if p_data in self.__text:
            self.setCurrentIndex(self.__text.index(p_data))
        elif p_data in self.__value:
            self.setCurrentIndex(self.__value.index(p_data))
        else:
            pass


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
        if p_data in self.__texts:
            self.setCurrentIndex(self.__texts.index(p_data))
        elif p_data in self.__names:
            self.setCurrentIndex(self.__names.index(p_data))
        else:
            pass


class SelectDictionary(OrcSelectBase):
    """
    字典下拉列表
    """
    def __init__(self, p_id, p_empty=False):

        OrcSelectBase.__init__(self, p_empty)

        self.__resource_dict = OrcResource('Dict')

        result = self.__resource_dict.get(parameter=dict(dict_flag=p_id))

        if not ResourceCheck.result_status(result, u'获取字典信息'):
            dict_result = list()
        else:
            dict_result = result.data

        dict_data = [dict(name=_item['dict_value'], text=_item['dict_text'])
                     for _item in dict_result]

        self._set_item_data(dict_data)


class SelectWidgetType(OrcSelectBase):
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

        from LibDict import LibDict

        self.__dict = LibDict()
        _data = [dict(name=_item.type_name, text=_item.type_text)
                 for _item in self.__dict.get_widget_type()]

        self._set_item_data(_data)


class SelectWidgetOperation(OrcSelectBase):
    """
    下拉控件类型列表
    """

    def __init__(self, p_empty=False):
        """
        User defined combobox, it's data is come from table lib_dictionary
        :param p_empty: 是否包含空值
        :return:
        """
        OrcSelectBase.__init__(self, p_empty)

        from LibDict import LibDict

        self.__dict = LibDict()

    def set_type(self, p_type):

        self.clear()

        # 获取当前控件的制作方式,去除不可操作控件
        if p_type in ("WINDOW", "GROUP"):
            return

        _data = [dict(name=_item.ope_name, text=_item.ope_text)
                 for _item in self.__dict.get_widget_operation(p_type)]

        # 获取基本操作方式
        if p_type not in ("PAGE", "BLOCK"):
            _data.extend([dict(name=_item.ope_name, text=_item.ope_text)
                          for _item in self.__dict.get_widget_operation("BLOCK")])

        self._set_item_data(_data)


def operate_to_str(p_data):
    """
    :param p_data: {'OBJECT': '3200000002', 'OPERATE': u'INPUT', 'TYPE': u'WIDGET'}
    :return:
    """
    if not isinstance(p_data, dict):
        return p_data

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
        resource_dict = OrcResource("Dict")
        result = resource_dict.get(parameter=dict(dict_flag=p_flag, dict_value=p_value))

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取操作文字"):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u"获取操作文字")

        return result.data[0]["dict_text"]

    _dict = LibDict()

    _type = p_data["TYPE"]
    _object = p_data["OBJECT"]

    if "WIDGET" == _type:

        _operation = p_data["OPERATION"]

        try:
            _object = get_widget_def_path(_object)
            _type = get_lib_dict_text("operate_object_type", _type)

            _operation = _dict.get_widget_operation_text(_operation)

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
    def __init__(self):

        QVBoxLayout.__init__(self)

        _label_type = QLabel(u"对象类型:")
        self.__type = SelectWidgetType()

        _layout_type = QHBoxLayout()
        _layout_type.addWidget(_label_type)
        _layout_type.addWidget(self.__type)

        _label_operate = QLabel(u"操作方式:")
        self.__operate = SelectWidgetOperation()

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


class OrcPagination(QWidget):
    sig_page = OrcSignal(tuple)

    def __init__(self):

        QWidget.__init__(self)

        self._message = QLabel()

        self._btn_first = QPushButton("F")
        self._btn_last = QPushButton("L")
        self._btn_previous = QPushButton("p")
        self._btn_next = QPushButton("n")

        self._jump = QComboBox()
        self._number = QLineEdit()
        self._number.setText("20")

        _layout = QHBoxLayout()
        _layout.addWidget(self._message)
        _layout.addWidget(self._btn_first)
        _layout.addWidget(self._btn_previous)
        _layout.addWidget(self._btn_next)
        _layout.addWidget(self._btn_last)
        _layout.addWidget(self._jump)
        _layout.addWidget(self._number)

        _layout.setContentsMargins(0, 0, 0, 0)
        _layout.setSpacing(0)

        self.setLayout(_layout)

        self._btn_first.clicked.connect(self.first_page)
        self._btn_last.clicked.connect(self.last_page)
        self._btn_previous.clicked.connect(self.previous_page)
        self._btn_next.clicked.connect(self.next_page)
        self._jump.currentIndexChanged.connect(self.jump_to_page)

        # 总页数
        self.__pages = 10

        #  当前页码
        self.__page = 1

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
