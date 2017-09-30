# coding=utf-8
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from OrcLib.LibCmd import WebCmd
from OrcWidget import WidgetBlock


class WidgetSelect(WidgetBlock):
    """
    Select 下拉框,选择方法有根据值来选择,根据顺序选择
    """
    def __init__(self, p_root, p_id):

        WidgetBlock.__init__(self, p_root, p_id)

    def execute(self, p_para):
        """
        运行
        :param p_para:
        :type p_para: WebCmd
        :return:
        """
        res = self.basic_execute(p_para)

        if res is not None:
            return res

        if "TEXT" == p_para.cmd_operation:

            try:
                # 获取 option
                opt = self._widget.find_element_by_xpath("option[text()='%s']" % p_para.data_num).get_attribute('value')

                # 根据 value 属性来选择
                Select(self._widget).select_by_value(opt)

            except NoSuchElementException:
                self._logger.error("未找到控件: TEXT--%s" % p_para.data_inp[0])
                return False

            return True

        elif "LABEL" == p_para.cmd_operation:

            try:
                # 获取 option
                opt = self._widget.find_element_by_xpath("option[@label='%s']" % p_para.data_num).get_attribute('value')

                # 根据 value 属性来选择
                Select(self._widget).select_by_value(opt)

            except NoSuchElementException:
                self._logger.error("未找到控件: LABEL--%s" % p_para.data_inp[0])
                return False

            return True

        elif "VALUE" == p_para.cmd_operation:

            # 根据 value 属性来选择
            Select(self._widget).select_by_value(p_para.data_inp[0])

            return True

        else:
            pass
