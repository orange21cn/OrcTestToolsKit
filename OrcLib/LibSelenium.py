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


def slm_input(p_inp, p_value):
    """
    input 输入数据
    :param p_value:
    :param p_inp:
    :return:
    """
    if p_inp.get_attribute("value") is not None:
        p_inp.clear()

    p_inp.send_keys(p_value)


def slm_click(p_inp):
    """
    Click
    :param p_inp:
    :return:
    """
    p_inp.click()
