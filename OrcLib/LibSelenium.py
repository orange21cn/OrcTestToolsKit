# coding=utf-8
from selenium.webdriver.support.ui import Select


def slm_select(p_sel, p_flg, p_value):
    """
    Select 选择
    :param p_sel:
    :param p_flg:
    :param p_value:
    :return:
    """
    cur_select = Select(p_sel)

    if "INDEX" == p_flg:
        cur_select.select_by_index(p_value)
    elif "VALUE" == p_flg:
        cur_value = p_sel.find_element_by_xpath("option[text()='" + p_value + "']").get_attribute("value")
        cur_select.select_by_value(cur_value)
    else:
        pass


def slm_click(p_inp):
    """
    Click
    :param p_inp:
    :return:
    """
    p_inp.click()
