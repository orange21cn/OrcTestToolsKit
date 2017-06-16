# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtCore import QModelIndex
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibViewDef import def_view_page_det
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
        self.display = ViewTable('PageDet', PageDetModel, PageDetControl)

        # Buttons widget
        wid_buttons = OrcButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK")
        ])

        # win_add
        self.__win_add = ViewAdd(def_view_page_det)

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

        # 新增
        self.__win_add.sig_submit[dict].connect(self.add)

    def operate(self, p_flag):
        """
        点击按钮操作
        :param p_flag:
        :return:
        """
        if "add" == p_flag:
            self.__win_add.show()
        elif "delete" == p_flag:
            if OrcMessage.question(self, u"确认删除"):
                self.display.model.mod_delete()
        elif "update" == p_flag:
            self.display.model.editable()
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

    def add_show(self):
        """
        显示新增界面
        :return:
        """
        if self.__page_id is not None:
            self.__win_add.show()

    def add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        _data = p_data
        _data["page_id"] = self.__page_id
        self.display.model.mod_add(_data)

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
