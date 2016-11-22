# -*- coding: utf-8 -*-
import logging
from OrcLib.LibNet import OrcReturn
from OrcLib.LibNet import allow_cross_domain
from OrcLib.LibNet import orc_get_parameter
from OrcApi.Batch.BatchDefModel import BatchDefModel
from OrcApi.Batch.BatchDetModel import BatchDetModel
from OrcApi.Case.CaseDefModel import CaseDefModel
from OrcApi import app


api_batch_log = logging.getLogger("api")


# ---- Batch definition ---------------------------------------------------------- #
@app.route("/BatchDef/usr_search", methods=['POST'])
@allow_cross_domain
def batch_search():
    """
    request: {id:..,batch_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = BatchDefModel()
    _value = _model.usr_search(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/BatchDef/usr_add", methods=['POST'])
@allow_cross_domain
def batch_add():
    """
    request: {id:..,batch_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = BatchDefModel()
    _value = _model.usr_add(_parameter)
    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/BatchDef/usr_modify", methods=['POST'])
@allow_cross_domain
def batch_modify():
    """
    request: {id:..,batch_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = BatchDefModel()
    _model.usr_modify(_parameter)

    return _return.get_return()


@app.route("/BatchDef/usr_delete", methods=['POST'])
@allow_cross_domain
def batch_delete():
    """
    request: {id:..,batch_no:....}
    :return:
    """
    i_parameter = orc_get_parameter()
    _return = OrcReturn()

    i_model = BatchDefModel()
    i_model.usr_delete(i_parameter)

    return _return.get_return()


@app.route("/BatchDef/usr_get_no", methods=['POST'])
@allow_cross_domain
def batch_get_no():
    """
    request: {id:..,batch_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = BatchDefModel()
    _res = _model.usr_get_value(_parameter)

    _return.set_str_result(_res.batch_no)

    return _return.get_return()


# ---- Batch detail ---------------------------------------------------------- #
@app.route("/BatchDet/usr_search", methods=['POST'])
@allow_cross_domain
def batch_det_search():
    """
    request: {id:..,batch_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model_batch = BatchDetModel()
    _model_case = CaseDefModel()

    _cond_batch = {}
    _cond_case = {}

    # Split search condition
    for t_id, t_value in _parameter.items():

        if "batch_id" == t_id:
            _cond_batch[t_id] = t_value
        else:
            _cond_case[t_id] = t_value

    # Search case list
    _value_batch = _model_batch.usr_search(_cond_batch)
    _cond_case["id"] = list(_item.case_id for _item in _value_batch)

    # Search case detail
    _value_case = _model_case.usr_list_search(_cond_case)

    # Connect data
    _res = []
    for t_batch_item in _value_batch:

        _data = {"id": t_batch_item.id,
                 "case_id": t_batch_item.case_id,
                 "create_time": t_batch_item.create_time.strftime("%Y-%m-%d %H:%M:%S")}
        for t_case_item in _value_case:

            if t_case_item.id == _data["case_id"]:

                _data["case_no"] = t_case_item.case_no
                _data["case_name"] = t_case_item.case_name

        _res.append(_data)

    # Set return data
    _return.set_arr_result(_res)

    return _return.get_return()


@app.route("/BatchDet/usr_add", methods=['POST'])
@allow_cross_domain
def batch_det_add():
    """
    request: {id:..,batch_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = BatchDetModel()
    _value = _model.usr_add(_parameter)
    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/BatchDet/usr_delete", methods=['POST'])
@allow_cross_domain
def batch_det_delete():
    """
    request: {id:..,batch_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = BatchDetModel()
    _value = _model.usr_delete(_parameter)
    _return.set_str_result(_value)

    return _return.get_return()
