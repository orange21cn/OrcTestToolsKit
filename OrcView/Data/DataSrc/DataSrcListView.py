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
    sig_selected = OrcSignal(str)

    def __init__(self):

        ViewTable.__init__(self, 'DataSrc', DataSrcListModel, DataSrcListControl)

        self.model.mod_search()

        self.clicked.connect(self.current_data)

    def current_data(self):
        """
        发送当前数据
        :return:
        """
        self.sig_selected.emit(self.model.mod_get_current_data()['id'])

    def editable(self, p_flag):
        """
        设置可编辑状态
        :param p_flag:
        :return:
        """
        self.model.checkable(p_flag)
        self.model.reset()
