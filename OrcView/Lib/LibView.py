# coding=utf-8
from PySide.QtCore import Signal as OrcSignal
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QLabel
from PySide.QtGui import QComboBox
from PySide.QtGui import QLineEdit
from PySide.QtGui import QTextEdit
from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import orc_db
from OrcLib.LibNet import orc_invoke
from OrcLib.LibException import OrcPostFailedException


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
        return OrcLineEdit(parent)

    # 多行输入框
    elif "TEXTAREA" == p_type["TYPE"]:
        if "SEARCH" == p_type["SOURCE"]:
            return OrcLineEdit(parent)
        else:
            return OrcTextArea(parent)

    # 时间显示
    elif "DATETIME" == p_type["TYPE"]:
        return OrcLineEdit(parent)

    # 选择输入框
    elif "SELECT" == p_type["TYPE"]:
        _view = OrcSelect(p_type["FLAG"])
        if "SEARCH" == p_type["SOURCE"]:
            _view.insertItem(0, u"所有", "")
        _view.setCurrentIndex(0)
        return _view

    # 其他
    elif "OPERATE" == p_type["TYPE"]:
        return OrcOperate(parent)

    # 其他
    else:
        return OrcLineEdit(parent)


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

    def __init__(self, parent):
        QLineEdit.__init__(self, parent)

    def get_data(self):
        return self.text()

    def set_data(self, p_data):
        return self.setText(p_data)


class OrcTextArea(QTextEdit):
    """
    多行输入框
    """

    def __init__(self, parent):
        QTextEdit.__init__(self, parent)

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
    下拉列表
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
            _items[0:0] = [LibDictionary(dict(dict_text="", dict_value=""))]

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


def operate_to_str(p_data):
    """
    :param p_data: {'OBJECT': '3200000002', 'OPERATE': u'INPUT', 'TYPE': u'WIDGET'}
    :return:
    """
    _widget_get_path = 'http://localhost:5000/WidgetDef/usr_get_path'
    _page_get_flag = 'http://localhost:5000/PageDef/usr_get_flag'
    _get_dict_text = 'http://localhost:5000/Lib/usr_get_dict_text'

    _type = p_data["TYPE"]
    _object = p_data["OBJECT"]

    if "WIDGET" == _type:

        _operate = p_data["OPERATE"]

        try:
            _object = orc_invoke(_widget_get_path, _object)
            if 0 < len(_object):
                _object = _object[0]["PATH"]
            _type = orc_invoke(_get_dict_text, dict(flag="operate_object_type", value=_type))
            _operate = orc_invoke(_get_dict_text, dict(flag="widget_operator", value=_operate))

        except OrcPostFailedException:
            # Todo
            pass

        return "%s|%s|%s" % (_operate, _type, _object)

    else:

        try:
            _object = orc_invoke(_page_get_flag, _object)
            if 0 < len(_object):
                _object = _object
            _type = orc_invoke(_get_dict_text, dict(flag="operate_object_type", value=_type))
        except OrcPostFailedException:
            # Todo
            print _object
            pass

        return "%s|%s" % (_type, _object)


class ObjectOperator(QVBoxLayout):

    def __init__(self):

        QVBoxLayout.__init__(self)

        _label_type = QLabel(u"对象类型:")
        self.__type = OrcSelect("operate_object_type")

        _layout_type = QHBoxLayout()
        _layout_type.addWidget(_label_type)
        _layout_type.addWidget(self.__type)

        _label_operate = QLabel(u"操作方式:")
        self.__operate = OrcSelect()

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
            self.__operate.set_flag("widget_operator")
        elif"PAGE" == _type:
            self.__operate.set_flag("page_operator")
        else:
            self.__operate.set_flag("")

    def get_data(self):

        _data = {"TYPE": self.__type.get_data()}

        if self.__operate.get_data() is not None:
            _data["OPERATE"] = self.__operate.get_data()

        return _data
