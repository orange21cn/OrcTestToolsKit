# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibTable import ViewTable

from .DataSrcListModel import DataSrcListModel


class DataSrcListControl(ControlBase):
    """

    """
    def __init__(self):

        ControlBase.__init__(self, 'DataSrc')


class DataSrcListView(ViewTable):
    """
    显示数据源列表
    """
    def __init__(self):

        ViewTable.__init__(self, DataSrcListModel, DataSrcListControl)

        self.model.mod_search()

    def editable(self, p_flag):
        """
        设置可编辑状态
        :param p_flag:
        :return:
        """
        self.model.basic_checkable(p_flag)
        self.model.reset()
