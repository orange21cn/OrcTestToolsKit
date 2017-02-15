# coding=utf-8
from OrcLib.LibProcess import get_widget_mark
from OrcLib.LibProcess import get_mark

from OrcView.Lib.LibViewDef import def_view_data
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.Driver.Web.WidgetSelect import ViewWidgetSelect

from DataModel import DataModel


class ViewDataAdd(ViewAdd):
    """
    View of table
    """
    def __init__(self):
        """
        :return:
        """
        ViewAdd.__init__(self, def_view_data)

        self.__model = DataModel()

        # 控件选择控件
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
        self.set_data("data_flag", (p_data["id"], get_widget_mark(p_data['id'])))

    def set_src_type(self, p_type):
        """
        设置数据源类型, SELECT
        :param p_type:
        :return:
        """
        self.set_data("src_type", p_type)
        self.set_enable("src_type", False)

    def set_src_id(self, p_id):
        """
        设置数据源标识, DISPLAY
        :param p_id:
        :return:
        """
        self.set_data("src_id", (p_id, get_mark(self.get_data('src_type'), p_id)))
        self.set_enable("src_id", False)

    def __save(self, p_data):
        """
        保存数据
        :param p_data:
        :return:
        """
        self.__model.service_add(p_data)
