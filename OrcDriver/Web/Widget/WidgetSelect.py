# coding=utf-8
from selenium.webdriver.support.ui import Select
from OrcWidget import OrcWidget


class WidgetSelect(OrcWidget):
    """
    Select 下拉框,选择方法有根据值来选择,根据顺序选择
    """
    def __init__(self, p_root, p_id):

        OrcWidget.__init__(self, p_root, p_id)

    def execute(self, p_para):

        res = self.basic_execute(p_para)

        if res is not None:
            return res

        _flag = p_para["OPERATION"]
        _data = None if "DATA" not in p_para else p_para["DATA"]

        if "SELECT" == _flag:

            # 获取 option
            opt = self._widget.find_element_by_xpath("option[@label='%s'" % _data).get_attribute('value')

            # 根据 value 属性来选择
            Select(self._widget).select_by_value(opt)

            return True

        else:
            pass
