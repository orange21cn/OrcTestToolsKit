# coding=utf-8
import json

from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QStackedWidget
from PySide.QtGui import QWidget

from OrcView.Case.Case.CaseView import CaseView
from OrcView.Data.Data.DataAdd import ViewDataAdd
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibViewDef import def_view_item
from .ItemModel import ItemFuncModel
from .ItemModel import ItemNormalModel
from .OperateView import ViewOperate


class ItemControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'Item')


class ItemView(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.__step_id = None

        # Current case id
        self.__step_type = None
        self.__win_operate = ViewOperate()

        # Item ----
        # 步骤项显示
        self.item_display = ViewTable('Item', ItemNormalModel, ItemControl)

        # Func --
        self.func_display = ViewTable('CaseDef', ItemFuncModel, ItemControl)

        # current display
        self.display = self.item_display

        # stack widget
        self.main_display = QStackedWidget()
        self.main_display.addWidget(self.item_display)
        self.main_display.addWidget(self.func_display)

        # Context menu
        menu_def = [dict(NAME=u"增加", STR="sig_add"),
                    dict(NAME=u"删除", STR="sig_del"),
                    dict(NAME=u"增加数据", STR="sig_data")]

        self.item_display.create_context_menu(menu_def)
        self.func_display.create_context_menu(menu_def)

        # Buttons widget
        wid_buttons = OrcButtons([
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="up", name=u"上移"),
            dict(id="down", name=u"下移"),
        ], "VER")

        # 新增 item 窗口
        self.__win_add_item = ViewAdd(def_view_item)

        # 新增 func 窗口
        self.__win_add_func = CaseView("SINGLE")

        # win add data
        self.__win_data = ViewDataAdd()

        # Layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.main_display)
        main_layout.addWidget(wid_buttons)

        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)

        # 显示操作选择框
        self.__win_add_item.sig_operate.connect(self.__win_operate.show)

        # 新增 item
        self.__win_add_item.sig_submit.connect(self.add_item)

        # 新增 func
        self.__win_add_func.sig_selected.connect(self.add_func)

        # 新增 operate
        self.__win_operate.sig_submit.connect(self.set_operate)

        # 点击按钮操作
        wid_buttons.sig_clicked.connect(self.operate)

        # 右键菜单
        self.item_display.sig_context.connect(self.context)
        self.func_display.sig_context.connect(self.context)

    def add_show(self):
        """
        显示增加界面
        :return:
        """
        if self.__step_id is not None:

            _type = self.display.model.service_get_step_type(self.__step_id)

            if "FUNC" == _type:
                self.__win_add_func.show()

            elif "NORMAL" == _type:
                self.__win_add_item.show()

            else:
                pass

    def add_item(self, p_data):
        """
        增加步骤项
        :param p_data:
        :return:
        """
        _data = dict(
            type="ITEM",
            step_id=self.__step_id,
            data=p_data
        )
        self.display.model.mod_add(_data)

    def add_func(self, p_data):
        """
        增加函数步骤
        :param p_data:
        :return:
        """
        _data = dict(
            type="FUNC",
            step_id=self.__step_id,
            data=p_data[0],
        )
        self.display.model.mod_add(_data)

    def set_step_id(self, p_step_id):
        """
        设置步骤ID
        :param p_step_id:
        :return:
        """
        self.__step_id = p_step_id
        step_type = self.display.model.service_get_step_type(self.__step_id)

        if "FUNC" == step_type:
            self.display = self.func_display
            self.main_display.setCurrentIndex(1)

        elif "NORMAL" == step_type:
            self.display = self.item_display
            self.main_display.setCurrentIndex(0)

        else:
            pass

        self.display.model.mod_search({"step_id": self.__step_id})

    def clean(self):
        """
        清理
        :return:
        """
        self.__step_id = None
        self.display.model.mod_clean()

    def operate(self, p_flag):
        """
        按钮操作
        :param p_flag:
        :return:
        """
        if "add" == p_flag:
            self.add_show()
        elif "delete" == p_flag:
            self.display.model.mod_delete()
        elif "update" == p_flag:
            self.display.model.editable()
        elif "up" == p_flag:
            self.display.model.mod_up()
        elif "down" == p_flag:
            self.display.model.mod_down()
        else:
            pass

    def context(self, p_flag):
        """
        右键菜单
        :param p_flag:
        :return:
        """
        if "sig_data" == p_flag:

            _id = self.display.model.mod_get_current_data()["item_id"]

            self.__win_data.show()
            self.__win_data.set_src_type("ITEM")
            self.__win_data.set_src_id(_id)

    def set_operate(self, p_data):
        """
        获取操作字符串
        :param p_data:
        :return:
        """
        self.__win_add_item.set_data("item_operate", json.loads(p_data))
