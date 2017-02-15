# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck


_logger = OrcLog('basic.process')


def get_mark(p_flag, p_id):
    """
    获取标识
    :param p_flag:
    :param p_id:
    :return:
    """
    if "BATCH" == p_flag:
        return get_batch_mark(p_id)
    elif "CASE" == p_flag:
        return get_case_mark(p_id)
    elif "STEP" == p_flag:
        return get_step_mark(p_id)
    elif "ITEM" == p_flag:
        return get_item_mark(p_id)
    elif "PAGE_DEF" == p_flag:
        return get_page_def_mark(p_id)
    elif "PAGE_DET" == p_flag:
        return get_page_det_mark(p_id)
    elif "WIDGET" == p_flag:
        return get_widget_mark(p_id)
    else:
        return None


def get_batch_mark(p_batch_id):
    """
    获取计划标识
    :param p_batch_id:
    :return:
    """
    resource_batch_def = OrcResource('BatchDef')

    # 获取计划信息
    batch_def_info = resource_batch_def.get(path=p_batch_id)

    if not ResourceCheck.result_status(batch_def_info, u'查询计划数据', _logger):
        return None

    if not batch_def_info.data:
        return None

    return batch_def_info.data['batch_no']


def get_case_mark(p_case_id):
    """
    获取用例显示标识
    :param p_case_id:
    :return:
    """
    resource_case_def = OrcResource('CaseDef')

    # 获取用例信息
    case_def_info = resource_case_def.get(path=p_case_id)

    if not ResourceCheck.result_status(case_def_info, u'查询用例数据', _logger):
        return None

    if not case_def_info.data:
        return None

    return case_def_info.data['case_path']


def get_step_mark(p_step_id):
    """
    获取步骤显示标识
    :param p_step_id:
    :return:
    """
    resource_case_det = OrcResource('CaseDet')

    # 获取用例步骤数据
    case_det_info = resource_case_det.get(parameter=dict(step_id=p_step_id))

    if not ResourceCheck.result_status(case_det_info, u'查询用例步骤数据', _logger):
        return None

    if not case_det_info.data:
        return None

    # 获取用例数据
    case_mark = get_case_mark(case_det_info.data[0]['case_id'])

    if case_mark is None:
        return None

    return "%s:%s" % (case_mark, case_det_info.data[0]['step_no'])


def get_item_mark(p_item_id):
    """
    获取执行项显示标识
    :param p_item_id:
    :return:
    """
    resource_step_det = OrcResource('StepDet')

    # 获取步骤步骤项数据
    step_det_info = resource_step_det.get(parameter=dict(item_id=p_item_id))

    if not ResourceCheck.result_status(step_det_info, u'查询步骤步骤项数据', _logger):
        return None

    if not step_det_info.data:
        return None

    # 获取步骤标识
    step_mark = get_step_mark(step_det_info.data[0]['step_id'])

    if step_mark is None:
        return None

    return "%s:%s" % (step_mark, step_det_info.data[0]['item_no'])


def get_page_def_mark(p_page_def_id):
    """
    获取页面显示标识
    :param p_page_def_id:
    :return:
    """
    resource_page_def = OrcResource('PageDef')

    # 获取 page_def 信息
    page_def_info = resource_page_def.get(path=p_page_def_id)

    if not ResourceCheck.result_status(page_def_info, u'查询页面数据', _logger):
        return None

    if not page_def_info.data:
        return None

    return page_def_info.data['page_flag']


def get_page_det_mark(p_page_det_id):
    """
    获取环境.页面显示标识
    :param p_page_det_id:
    :return:
    """
    resource_page_det = OrcResource('PageDet')
    resource_dict = OrcResource('Dict')

    # 查询环境页面信息
    page_det_info = resource_page_det.get(path=p_page_det_id)

    if not ResourceCheck.result_status(page_det_info, u'查询环境页面信息', _logger):
        return None

    if not page_det_info.data:
        return None

    # 查询页面信息
    page_def_info = get_page_def_mark(page_det_info.data['page_id'])

    if not ResourceCheck.result_status(page_det_info, u'查询页面信息', _logger):
        return None

    if not page_det_info.data:
        return None

    # 查询环境信息
    env_info = resource_dict.get(parameter=dict(dict_flag='test_env', dict_value=page_det_info.data['page_env']))

    if not env_info:
        return None

    return "%s:%s" % (env_info.data[0]['dict_text'], page_def_info)


def get_widget_mark(p_widget_id):
    """
    获取控件显示标识
    :param p_widget_id:
    :return:
    """
    resource_widget_def = OrcResource("WidgetDef")

    # 查询控件信息
    widget_def_info = resource_widget_def.get(path=p_widget_id)

    if not ResourceCheck.result_status(widget_def_info, u'查询控件信息', _logger):
        return None

    if not widget_def_info.data:
        return None

    return widget_def_info.data['widget_path']
