from OrcWidget import OrcWidget


class WidgetButton(OrcWidget):

    def __init__(self, p_root, p_id):

        OrcWidget.__init__(self, p_root, p_id)

    def execute(self, p_para):

        res = self.basic_execute(p_para)

        if res is not None:
            return res
