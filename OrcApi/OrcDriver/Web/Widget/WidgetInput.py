from OrcWidget import WidgetBlock
from OrcLib.LibCmd import WebCmd


class WidgetInput(WidgetBlock):

    def __init__(self, p_root, p_id):

        WidgetBlock.__init__(self, p_root, p_id)

    def execute(self, p_para):
        """

        :param p_para:
        :type p_para: WebCmd
        :return:
        """
        res = self.basic_execute(p_para)

        if res is not None:
            return res

        if "INPUT" == p_para.cmd_operation:

            if self._widget.get_attribute("value") is not None:
                self._widget.clear()

            self._widget.send_keys(str(p_para.data_inp[0]))

            return True

        else:
            pass
