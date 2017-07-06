# coding=utf-8
from .OrcWidget import OrcWidget


class WidgetAlert(OrcWidget):

    def __init__(self, p_root):

        OrcWidget.__init__(self, p_root, None)

    def execute(self, p_para):
        """
        执行
        :param p_para:
        :return:
        """
        self._widget = self._widget.switch_to.alert

        _flag = p_para["OPERATION"]

        if 'ACCEPT' == _flag:
            self._widget.accept()
        elif 'DISMISS' == _flag:
            self._widget.dismiss()
        else:
            pass
