# coding=utf-8
from selenium.webdriver.common.action_chains import ActionChains

from OrcWidget import WidgetBlock
from OrcLib.LibCmd import WebCmd


class WidgetMulti(WidgetBlock):

    def __init__(self, p_root, p_id):

        WidgetBlock.__init__(self, p_root, p_id)

        self._widget_from = self._widget
        self._widget_to = None

        if 2 == len(self._ids):
            self._get_widget()
            self._widget_to = self._widget

    def execute(self, p_para):
        """
        操作
        :param p_para:
        :type p_para: WebCmd
        :return:
        """
        if 'DRAG_AND_DROP' == p_para.cmd_operation:
            ActionChains(self._root).drag_and_drop(self._widget_from, self._widget_to)

        else:
            pass
