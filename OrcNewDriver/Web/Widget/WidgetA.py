from OrcWidget import WidgetBlock


class WidgetA(WidgetBlock):

    def __init__(self, p_root, p_id):

        WidgetBlock.__init__(self, p_root, p_id)

    def execute(self, p_para):
        print "--------"
        res = self.basic_execute(p_para)
        print "----", res
        if res is not None:
            return res