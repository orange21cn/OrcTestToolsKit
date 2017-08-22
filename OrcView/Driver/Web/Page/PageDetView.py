# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibAdd import ViewNewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibMessage import OrcMessage

from .PageDetModel import PageDetModel


class PageDetControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'PageDet')


class PageDetView(QWidget):
    """

    """
    sig_selected = OrcSignal(str)

    def __init__(self):

        QWidget.__init__(self)

        # Current page id
        self.__page_id = None

        # Data result display widget
        self.display = ViewTable(PageDetModel, PageDetControl)

        # Buttons widget
        wid_buttons = OrcButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK")
        ])

        # Layout
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.display)
        layout_main.addWidget(wid_buttons)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # 点击按钮操作
        wid_buttons.sig_clicked.connect(self.operate)

        # 单击发送点击事件
        self.display.clicked[QModelIndex].connect(self.page_select)

    def operate(self, p_flag):
        """
        点击按钮操作
        :param p_flag:
        :return:
        """
        if "add" == p_flag:
            if self.__page_id is None:
                return
            _data = PageDetAdder.static_get_data()
            if _data is not None:
                _data["page_id"] = self.__page_id
                self.display.model.mod_add(_data)
        elif "delete" == p_flag:
            if OrcMessage.question(self, u"确认删除"):
                self.display.model.mod_delete()
        elif "update" == p_flag:
            self.display.model.basic_editable()
        else:
            pass

    def page_select(self, p_index):
        """
        发送点击事件
        :param p_index:
        :return:
        """
        page_det_id = self.display.model.mod_get_data(p_index.row())["id"]
        self.sig_selected.emit(page_det_id)

    def set_page_id(self, p_page_id):
        """
        设置页面 id
        :param p_page_id:
        :return:
        """
        self.__page_id = p_page_id
        self.display.model.mod_search({"page_id": self.__page_id})

    def clean(self):
        """
        清理
        :return:
        """
        self.display.model.mod_clean()


class PageDetAdder(ViewNewAdd):
    """
    新增计划控件
    """
    def __init__(self):

        ViewNewAdd.__init__(self, 'PageDet')

        self.setWindowTitle(u'新增页面')

    @staticmethod
    def static_get_data():

        view = PageDetAdder()
        view.exec_()

        return view._data
