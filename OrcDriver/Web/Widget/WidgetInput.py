from OrcWidget import OrcWidget


class WidgetInput(OrcWidget):

    def __init__(self, p_root, p_id):

        OrcWidget.__init__(self, p_root, p_id)

    def execute(self, p_para):

        _flag = p_para["OPERATION"]
        _data = p_para["DATA"]

        if "INPUT" == _flag:

            if self._widget.get_attribute("value") is not None:
                self._widget.clear()

            self._widget.send_keys(_data)

            return None
