from OrcDriver.Web.Widget.OrcWidget import OrcWidget


class WidgetButton(OrcWidget):

    def __init__(self, p_root, p_id):

        OrcWidget.__init__(self, p_root, p_id)

    def execute(self, p_para):

        _flag = p_para["OPERATION"]

        if "EXISTS" == _flag:

            return self.exists()

        elif "CLICK" == _flag:

            self._widget.click()

        else:
            pass
