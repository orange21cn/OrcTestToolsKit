# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibView import OrcPagination


class RunDataDispControl(ControlBase):
    """

    """
    def __init__(self):

        ControlBase.__init__(self, 'Data')


class RunDataDispModel(ModelTable):
    """

    """
    def __init__(self):

        ModelTable.__init__(self, 'Data')

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource.get(dict(
            CMD='SEARCH',
            TABLE='RunData',
            PARA=dict()
        ))

        return eval(result)

    def service_update(self, p_data):
        """
        更新,暂时不用
        :param p_data:
        :return:
        """
        pass

    def service_delete(self, p_list):
        """
        删除,暂时不用
        :param p_list:
        :return:
        """
        pass

    def service_add(self, p_data):
        """
        新增,暂时不用
        :param p_data:
        :return:
        """
        pass


class RunDataDispView(QWidget):
    """

    """
    def __init__(self):

        QWidget.__init__(self)

        # 数据显示
        self.display = ViewTable('Data', RunDataDispModel, RunDataDispControl)

        # 按钮
        self.__wid_buttons = OrcButtons([
            dict(id="update", name=u"更新"),
            dict(id="auto", name=u"自动更新", type="CHECK")
        ], p_align="FRONT")

        # 分页
        self.__wid_pagination = OrcPagination()

        # 底部
        layout_bottom = QHBoxLayout()
        layout_bottom.addWidget(self.__wid_buttons)
        layout_bottom.addWidget(self.__wid_pagination)

        # 整体布局
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.display)
        layout_main.addLayout(layout_bottom)

        self.setLayout(layout_main)
