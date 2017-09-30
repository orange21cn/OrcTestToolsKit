# coding=utf-8
from .OrcWidget import OrcWidget
from OrcLib.LibCmd import WebCmd


class WidgetAlert(OrcWidget):

    def __init__(self, p_root):

        OrcWidget.__init__(self, p_root, None)

    def execute(self, p_para):
        """
        执行
        :param p_para:
        :type p_para: WebCmd
        :return:
        """
        self._widget = self._widget.switch_to.alert

        _flag = p_para.cmd_operation

        if 'ACCEPT' == _flag:
            self._widget.accept()
        elif 'DISMISS' == _flag:
            self._widget.dismiss()
        else:
            pass
