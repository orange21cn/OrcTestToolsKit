# -*- coding: utf-8 -*-
from OrcLib.LibNet import OrcReturn
from OrcLib.LibNet import allow_cross_domain
from OrcLib.LibNet import orc_get_parameter
from OrcApi.Data.DataModel import DataHandle
from OrcApi import app


@app.route("/Data/usr_search", methods=['POST'])
@allow_cross_domain
def data_search():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = DataHandle()
    _value = _model.usr_search(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/Data/usr_add", methods=['POST'])
@allow_cross_domain
def data_add():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = DataHandle()
    _value = _model.usr_add(_parameter)

    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/Data/usr_delete", methods=['POST'])
@allow_cross_domain
def data_delete():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = DataHandle()
    _value = _model.usr_delete(_parameter)

    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/Data/usr_modify", methods=['POST'])
@allow_cross_domain
def data_modify():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = DataHandle()
    _value = _model.usr_modify(_parameter)

    _return.set_str_result(_value)

    return _return.get_return()
