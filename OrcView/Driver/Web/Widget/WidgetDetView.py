# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibAdd import ViewNewAdd
from OrcView.Lib.LibMessage import OrcMessage

from .WidgetDetModel import WidgetDetModel


class WidgetDetControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'WidgetDet')


class WidgetDetView(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        # Current widget id
        self.__widget_info = None

        # Data result display widget
        self.display = ViewTable(WidgetDetModel, WidgetDetControl)

        # Buttons widget
        wid_buttons = OrcButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="up", name=u"上移"),
            dict(id="down", name=u"下移")
        ])

        # Layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # 点击按钮
        wid_buttons.sig_clicked.connect(self.operate)

    def set_widget(self, p_widget_info):
        """
        设置控件 id
        :param p_widget_info:
        :return:
        """

        self.__widget_info = p_widget_info
        self.display.model.mod_search({"widget_id": self.__widget_info['id']})

    def clean(self):
        """
        清空
        :return:
        """
        self.__widget_info = None
        self.display.model.mod_clean()

    def operate(self, p_flag):
        """
        点击按钮操作
        :param p_flag:
        :return:
        """
        if "add" == p_flag:
            if self.__widget_info is None:
                return
            _data = WidgetDetAdder.static_get_data()
            if _data is not None:
                _data["widget_id"] = self.__widget_info['id']
                self.display.model.mod_add(_data)
        elif "delete" == p_flag:
            if OrcMessage.question(self, u"确认删除"):
                self.display.model.mod_delete()
        elif "update" == p_flag:
            self.display.model.basic_editable()
        elif "up" == p_flag:
            self.display.model.mod_up()
        elif "down" == p_flag:
            self.display.model.mod_down()
        else:
            pass


class WidgetDetAdder(ViewNewAdd):
    """
    新增计划控件
    """
    def __init__(self):

        ViewNewAdd.__init__(self, 'WidgetDet')

        self.setWindowTitle(u'新增控件属性')

    @staticmethod
    def static_get_data():

        view = WidgetDetAdder()
        view.exec_()

        return view._data
