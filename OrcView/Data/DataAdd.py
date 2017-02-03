# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibViewDef import def_view_data
from OrcView.Lib.LibAdd import ViewAdd

from DataService import DataService
from OrcView.Driver.Web.WidgetSelect import ViewWidgetSelect


class ViewDataAdd(ViewAdd):
    """
    View of table
    """
    # sig_data_flag = OrcSignal()

    def __init__(self):
        """
        :return:
        """
        ViewAdd.__init__(self, def_view_data)

        self.__service = DataService()
        self.__id = None

        # 选择控件
        self.__widget_select = ViewWidgetSelect()

        # 控件被点击
        self.sig_clicked.connect(self.__action)

        # 控件选取后设置数据标识
        self.__widget_select.sig_selected.connect(self.set_flag)

        # 提交操作
        self.sig_submit.connect(self.__save)

    def __action(self, p_flag):
        """
        控件被点击时的操作
        :param p_flag:
        :return:
        """
        if "data_flag" == p_flag:
            self.__widget_select.show()

    def set_flag(self, p_data):
        """
        设置数据标识
        :param p_data:
        :return:
        """
        self.set_data("data_flag", p_data["id"])
        self.set_enable("data_flag", False)

    def set_type(self, p_type):
        """
        设置数据类型
        :param p_type:
        :return:
        """
        self.set_data("src_type", p_type)
        self.set_enable("src_type", False)

    def set_path(self, p_path):
        """
        设置数据路径
        :param p_path:
        :return:
        """
        self.set_data("src_id", p_path)
        self.set_enable("src_id", False)

    def set_id(self, p_id):
        """
        设置数据 id
        :param p_id:
        :return:
        """
        self.__id = p_id

    def __save(self, p_data):
        """
        保存数据
        :param p_data:
        :return:
        """
        p_data["src_id"] = self.__id
        self.__service.usr_add(p_data)
