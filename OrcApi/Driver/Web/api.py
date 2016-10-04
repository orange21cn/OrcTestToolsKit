# -*- coding: utf-8 -*-
from OrcLib.LibNet import OrcReturn
from OrcLib.LibNet import allow_cross_domain
from OrcLib.LibNet import orc_get_parameter
from OrcLib.LibLog import OrcLog
from OrcApi.Driver.Web.PageDefModel import PageDefHandle
from OrcApi.Driver.Web.PageDetModel import PageDetHandle
from OrcApi.Driver.Web.WidgetDefModel import WidgetDefHandle
from OrcApi.Driver.Web.WidgetDetModel import WidgetDetHandle
from OrcApi.Driver.Web.WindowDefModel import WindowDefModel
from OrcApi import app


_logger = OrcLog("api.driver.web")


# ---- Page definition ---------------------------------------------------------- #
@app.route("/PageDef/usr_get_flag", methods=['POST'])
@allow_cross_domain
def page_def_get_flag():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = PageDefHandle()
    _value = _model.usr_search(_parameter)

    if 0 < len(_value):
        _result = _value[0].page_flag
    else:
        _result = None

    _return.set_str_result(_result)

    return _return.get_return()


@app.route("/PageDef/usr_add", methods=['POST'])
@allow_cross_domain
def page_def_add():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = PageDefHandle()
    _value = _model.usr_add(_parameter)

    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/PageDef/usr_delete", methods=['POST'])
@allow_cross_domain
def page_def_delete():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = PageDefHandle()
    _value = _model.usr_delete(_parameter)

    # 查询控件定义

    # 删除控件定义

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/PageDef/usr_modify", methods=['POST'])
@allow_cross_domain
def page_def_modify():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = PageDefHandle()
    _value = _model.usr_modify(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/PageDef/usr_search", methods=['POST'])
@allow_cross_domain
def page_def_search():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = PageDefHandle()
    _value = _model.usr_search(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


# ---- Page detail ---------------------------------------------------------- #
@app.route("/PageDet/usr_add", methods=['POST'])
@allow_cross_domain
def page_det_add():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = PageDetHandle()
    _value = _model.usr_add(_parameter)

    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/PageDet/usr_delete", methods=['POST'])
@allow_cross_domain
def page_det_delete():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = PageDetHandle()
    _value = _model.usr_delete(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/PageDet/usr_modify", methods=['POST'])
@allow_cross_domain
def page_det_modify():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = PageDetHandle()
    _value = _model.usr_modify(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/PageDet/usr_search", methods=['POST'])
@allow_cross_domain
def page_det_search():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = PageDetHandle()
    _value = _model.usr_search(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


# ---- Widget definition ---------------------------------------------------------- #
@app.route("/WidgetDef/usr_search", methods=['POST'])
@allow_cross_domain
def widget_def_search():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDefHandle()
    _value = _model.usr_search(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/WidgetDef/usr_search_all", methods=['POST'])
@allow_cross_domain
def widget_def_search_all():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDefHandle()
    _value = _model.usr_search_all(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/WidgetDef/usr_search_tree", methods=['POST'])
@allow_cross_domain
def widget_def_search_tree():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDefHandle()
    _value = _model.usr_search_tree(_parameter["id"])

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/WidgetDef/usr_add", methods=['POST'])
@allow_cross_domain
def widget_def_add():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDefHandle()
    _value = _model.usr_add(_parameter)
    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/WidgetDef/usr_delete", methods=['POST'])
@allow_cross_domain
def widget_def_delete():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDefHandle()
    _value = _model.usr_delete(_parameter)
    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/WidgetDef/usr_modify", methods=['POST'])
@allow_cross_domain
def widget_def_modify():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDefHandle()
    _value = _model.usr_modify(_parameter)
    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/WidgetDef/usr_get_path", methods=['POST'])
@allow_cross_domain
def widget_def_get_path():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDefHandle()
    _path = []

    if isinstance(_parameter, list):
        for t_id in _parameter:
            _item = dict(ID=t_id, PATH=_model.usr_get_path(t_id))
            _path.append(_item)
    else:
        _item = dict(ID=_parameter, PATH=_model.usr_get_path(_parameter))
        _path.append(_item)

    _return.set_arr_result(_path)

    return _return.get_return()


# ---- Widget detail ---------------------------------------------------------- #
@app.route("/WidgetDet/usr_search", methods=['POST'])
@allow_cross_domain
def widget_det_search():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDetHandle()
    _value = _model.usr_search(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/WidgetDet/usr_add", methods=['POST'])
@allow_cross_domain
def widget_det_add():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDetHandle()
    _value = _model.usr_add(_parameter)

    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/WidgetDet/usr_delete", methods=['POST'])
@allow_cross_domain
def widget_det_delete():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDetHandle()
    _value = _model.usr_delete(_parameter)

    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/WidgetDet/usr_modify", methods=['POST'])
@allow_cross_domain
def widget_det_modify():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WidgetDetHandle()
    _value = _model.usr_modify(_parameter)
    _return.set_str_result(_value)

    return _return.get_return()


# ---- Widget detail ---------------------------------------------------------- #
@app.route("/WindowDef/usr_search", methods=['POST'])
@allow_cross_domain
def window_def_search():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WindowDefModel()
    _value = _model.usr_search(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/WindowDef/usr_add", methods=['POST'])
@allow_cross_domain
def window_def_add():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WindowDefModel()
    _value = _model.usr_add(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/WindowDef/usr_modify", methods=['POST'])
@allow_cross_domain
def window_def_modify():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WindowDefModel()
    _value = _model.usr_modify(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/WindowDef/usr_delete", methods=['POST'])
@allow_cross_domain
def window_def_delete():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = WindowDefModel()
    _value = _model.usr_delete(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


# ---- Page ---------------------------------------------------------- #
# @app.route("/Page/usr_get_url", methods=['POST'])
# @allow_cross_domain
# def page_get_url():
#     """
#     Get page url by page detail id
#     :return:
#     """
#     _return = OrcReturn()
#
#     # input
#     _parameter = orc_get_parameter()
#     _logger.debug(_parameter)
#
#     _model_page_det = PageDetHandle()
#
#     _page_def = _model_page_det.usr_search(_parameter)
#     if 0 < len(_page_def):
#         _page_url = _page_def[0].page_url
#     else:
#         _page_url = None
#
#     # output
#     _logger.debug(_page_url)
#     _return.set_str_result(_page_url)
#
#     return _return.get_return()


# ---- Widget ---------------------------------------------------------- #
# @app.route("/Widget/usr_get_def", methods=['POST'])
# @allow_cross_domain
# def widget_get_def():
#     """
#     :return: list or None
#     """
#     _return = OrcReturn()
#
#     # Input
#     _parameter = orc_get_parameter()
#     _logger.debug(_parameter)
#
#     _model_widget_def = WidgetDefHandle()
#
#     _widget_def = _model_widget_def.usr_search(_parameter)
#
#     # Set result to None if definition is not exists, replace [] to None
#     if 0 < len(_widget_def):
#         _res = _widget_def
#     else:
#         _res = None
#
#     # Output
#     _logger.debug(_res)
#     _return.set_db_result(_res)
#
#     return _return.get_return()
#
#
# @app.route("/Widget/usr_get_det", methods=['POST'])
# @allow_cross_domain
# def widget_get_det():
#     """
#     :return: list or None
#     """
#     _return = OrcReturn()
#
#     # Input
#     _parameter = orc_get_parameter()
#     _logger.debug(_parameter)
#
#     _model_widget_det = WidgetDetHandle()
#
#     _widget_det = _model_widget_det.usr_search(_parameter)
#
#     # Set result to None if detail is not exists, replace [] to None
#     if 0 < len(_widget_det):
#         _res = _widget_det
#     else:
#         _res = None
#
#     # Output
#     _logger.debug(_res)
#     _return.set_db_result(_widget_det)
#
#     return _return.get_return()
