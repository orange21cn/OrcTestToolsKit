# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QSizePolicy
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QComboBox
from PySide.QtGui import QLineEdit
from PySide.QtGui import QTextEdit
from PySide.QtGui import QProgressBar

from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import orc_db
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibException import OrcPostFailedException
from LibDict import LibDict


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


class OrcTextArea(QTextEdit):
    """
    多行输入框
    """

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def get_data(self):
        return self.toPlainText()

    def set_data(self, p_data):
        self.setText(p_data)


class OrcOperate(QLineEdit):

    sig_operate = OrcSignal()

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

    def set_item_data(self, p_data=None):
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
    def __init__(self):
        OrcSelectBase.__init__(self)
        # Todo
        pass


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

        self.set_item_data(_data)


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
        print _data

        # 获取基本操作方式
        if p_type not in ("PAGE", "BLOCK"):
            _data.extend([dict(name=_item.ope_name, text=_item.ope_text)
                         for _item in self.__dict.get_widget_operation("BLOCK")])

        self.set_item_data(_data)


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
        resource_widget_def = OrcHttpResource("WidgetDef")
        resource_widget_def.set_path(p_id)

        widget_def_data = resource_widget_def.get()

        return None if not resource_widget_def else widget_def_data["widget_path"]

    def get_page_def_flag(p_id):
        """
        获取页面标识
        :param p_id:
        :return:
        """
        resource_page_def = OrcHttpResource("PageDef")
        resource_page_def.set_path(p_id)

        page_def_data = resource_page_def.get()

        return None if not page_def_data else page_def_data["page_flag"]

    def get_lib_dict_text(p_flag, p_value):
        """
        获取操作文字
        :param p_value:
        :param p_flag:
        :return:
        """
        resource_dict = OrcHttpResource("Dict")
        dict_data = resource_dict.get(dict(dict_flag=p_flag, dict_value=p_value))

        return None if not dict_data else dict_data[0]["dict_text"]

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

        self.__steps = p_steps

        self.__length = 100 / self.__steps
        self.__value = 0

        self.setValue(0)

    def step_forward(self):

        self.__value += self.__length

        if 100 - self.__value <= self.__length:
            self.__value = 100

        self.setValue(self.__value)
