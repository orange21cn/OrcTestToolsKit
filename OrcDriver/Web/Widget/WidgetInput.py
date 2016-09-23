from OrcWidget import OrcWidget


class WidgetInput(OrcWidget):

    def __init__(self, p_root, p_def):

        OrcWidget.__init__(self, p_root, p_def)

    def execute(self, p_flg, p_para):

        if "INPUT" == p_flg:

            if self._widget.get_attribute("value") is not None:
                self._widget.clear()

            self._widget.send_keys(p_para)

            return None
