
class WidgetButton:

    def __init__(self, p_widget):

        self.__widget = p_widget

    def execute(self, p_flg):

        if "CLICK" == p_flg:
            self.__widget.click()
