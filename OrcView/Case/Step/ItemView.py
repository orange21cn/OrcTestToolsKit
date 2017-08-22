# coding=utf-8

from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QStackedWidget
from PySide.QtGui import QWidget

from OrcLib.LibType import DriverType
from OrcView.Case.Case.CaseSelector import CaseSelector
from OrcView.Data.Data.DataAdd import DataAdder
from OrcView.Driver.Cmd.CmdCreator import DataCmdCreator
from OrcView.Driver.Cmd.CmdCreator import WebCmdCreator
from OrcView.Lib.LibAdd import ViewNewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTable import ViewTable

from .ItemModel import ItemFuncModel
from .ItemModel import ItemNormalModel


class ItemControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'Item')


class ItemView(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.__step_id = None

        # Current case id
        self.__step_type = None

        # Item ----
        # 步骤项显示
        self.item_display = ViewTable(ItemNormalModel, ItemControl)

        # Func --
        self.func_display = ViewTable(ItemFuncModel, ItemControl)

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

        # Layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.main_display)
        main_layout.addWidget(wid_buttons)

        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)

        # 点击按钮操作
        wid_buttons.sig_clicked.connect(self.operate)

        # 右键菜单
        self.item_display.sig_context.connect(self.context)
        self.func_display.sig_context.connect(self.context)

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

        if "STEP_FUNC" == step_type:
            self.display = self.func_display
            self.main_display.setCurrentIndex(1)

        elif "STEP_NORMAL" == step_type:
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

            if self.__step_id is None:
                return

            _type = self.display.model.service_get_step_type(self.__step_id)

            if "STEP_FUNC" == _type:
                _data = CaseSelector.static_get_data()
                if _data is not None:
                    self.add_func(_data)

            elif "STEP_NORMAL" == _type:
                _data = ItemAdder.static_get_data()
                if _data is not None:
                    self.add_item(_data)

            else:
                pass

        elif "delete" == p_flag:
            if OrcMessage.question(self, u'确认删除'):
                self.display.model.mod_delete()
        elif "update" == p_flag:
            self.display.model.basic_editable()
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
            DataAdder.static_add_data("ITEM", _id)


class ItemAdder(ViewNewAdd):
    """
    新增计划控件
    """
    def __init__(self):

        ViewNewAdd.__init__(self, 'Item')

        self.setWindowTitle(u'新增步骤项')

    def _action(self, p_flag):
        """
        点击控件后操作
        :param p_flag:
        :return:
        """
        if 'item_operate' == p_flag:

            item_mode = self.get_data('item_mode')
            item_type = self.get_data('item_type')

            if item_type == DriverType.WEB:
                cmd = WebCmdCreator.get_cmd(item_mode)
            elif item_type == DriverType.DATA:
                cmd = DataCmdCreator.get_cmd(item_mode)
            else:
                cmd = None

            self.set_data("item_operate", cmd)

    @staticmethod
    def static_get_data():

        view = ItemAdder()
        view.exec_()
        print "abcdef", view._data
        return view._data
