# -*- coding: utf-8 -*-
from OrcLib.LibNet import OrcReturn
from OrcLib.LibNet import allow_cross_domain
from OrcLib.LibNet import orc_get_parameter
from OrcApi.Case.CaseDefModel import CaseDefHandle
from OrcApi.Case.CaseDetModel import CaseDetHandle
from OrcApi.Case.StepDefModel import StepDefHandle
from OrcApi.Case.StepDetModel import StepDetHandle
from OrcApi.Case.ItemModel import ItemHandle
from OrcApi import app


# ---- Case Definition ---------------------------------------------------------- #
@app.route("/CaseDef/usr_search", methods=['POST'])
@allow_cross_domain
def case_def_search():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = CaseDefHandle()
    _value = _model.usr_search(_parameter)

    _return.set_db_result(_value)

    return _return.get_return()


@app.route("/CaseDef/usr_add", methods=['POST'])
@allow_cross_domain
def case_def_add():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = CaseDefHandle()
    _value = _model.usr_add(_parameter)

    _return.set_str_result(_value)

    return _return.get_return()


@app.route("/CaseDef/usr_modify", methods=['POST'])
@allow_cross_domain
def case_def_modify():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = CaseDefHandle()
    _model.usr_modify(_parameter)

    return _return.get_return()


@app.route("/CaseDef/usr_delete", methods=['POST'])
@allow_cross_domain
def case_def_delete():
    """
    request: {id:..,case_no:....}
    :return:
    """
    i_parameter = orc_get_parameter()
    _return = OrcReturn()

    i_model = CaseDefHandle()
    i_model.usr_delete(i_parameter)

    return _return.get_return()


@app.route("/CaseDef/usr_get_path", methods=['POST'])
@allow_cross_domain
def case_def_get_path():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = CaseDefHandle()
    _path = []

    if isinstance(_parameter, list):
        for t_id in _parameter:
            _item = dict(ID=t_id, PATH=_model.usr_get_path(t_id))
            _path.append(_item)
        _return.set_arr_result(_path)
    else:
        _path = _model.usr_get_path(_parameter)
        _return.set_str_result(_path)

    return _return.get_return()


# ---- Step ---------------------------------------------------------- #
@app.route("/CaseDet/usr_search", methods=['POST'])
@allow_cross_domain
def case_det_search():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model_case = CaseDetHandle()
    _model_step = StepDefHandle()

    _cond_case = {}
    _cond_step = {}

    # Split search condition
    for t_id, t_value in _parameter.items():

        if "case_id" == t_id:
            _cond_case[t_id] = t_value
        else:
            _cond_step[t_id] = t_value

    # Search step list
    _value_case = _model_case.usr_search(_cond_case)
    _cond_step["id"] = list(_item.step_id for _item in _value_case)

    # Search step detail
    _value_step = _model_step.usr_list_search(_cond_step)

    # Connect data
    _res = _connect(_value_case, _value_step, "step_id")

    # Set return data
    _return.set_arr_result(_res)

    return _return.get_return()


@app.route("/CaseDet/usr_add", methods=['POST'])
@allow_cross_domain
def case_det_add():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model_case = CaseDetHandle()
    _model_step = StepDefHandle()

    # Split condition
    _rtn = _parameter["case_det"]
    _cond_step = _parameter["step"]

    # Add step
    _step_id = _model_step.usr_add(_cond_step)

    # Add case detail
    _cond_case = dict(_rtn, **dict(step_id=_step_id["id"]))

    _model_case.usr_add(_cond_case)

    # Set return data
    _return.set_str_result(_rtn)

    return _return.get_return()


@app.route("/CaseDet/usr_delete", methods=['POST'])
@allow_cross_domain
def case_det_delete():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model_case = CaseDetHandle()

    _list_case_det = _parameter["list"]

    # Remove case detail list
    _model_case.usr_delete(_list_case_det)

    # Set return data
    _return.set_str_result("")

    return _return.get_return()


@app.route("/CaseDet/usr_modify", methods=['POST'])
@allow_cross_domain
def case_det_modify():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model_case = CaseDetHandle()
    _model_step = StepDefHandle()

    _cond_case = dict(id=_parameter["id"])
    _cond_step = _parameter

    # Get step id
    _step = _model_case.usr_search(_cond_case)
    _cond_step["id"] = _step[0].step_id

    # Search step detail
    _model_step.usr_modify(_cond_step)

    # Set return data
    _return.set_str_result("")

    return _return.get_return()


# ---- Item ---------------------------------------------------------- #
@app.route("/StepDet/usr_add", methods=['POST'])
@allow_cross_domain
def step_det_add():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model_step = StepDetHandle()
    _model_item = ItemHandle()

    _cond = _parameter

    # Add item
    _item_id = _model_item.usr_add(_cond)
    _cond["item_id"] = _item_id["id"]

    # Add step
    _step_det_id = _model_step.usr_add(_cond)

    # Set return data
    _return.set_str_result(_step_det_id)

    return _return.get_return()


@app.route("/StepDet/usr_delete", methods=['POST'])
@allow_cross_domain
def step_det_delete():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model_step_det = StepDetHandle()
    _cond_step_det = _parameter

    # Delete steps
    _model_step_det.usr_delete(_cond_step_det)

    # Set return data
    _return.set_arr_result("")

    return _return.get_return()


@app.route("/StepDet/usr_modify", methods=['POST'])
@allow_cross_domain
def step_det_modify():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model_step = StepDetHandle()
    _model_item = ItemHandle()

    _cond_step = dict(id=_parameter["id"])
    _cond_item = _parameter

    # Get item id
    _step = _model_step.usr_search(_cond_step)

    _cond_item["id"] = _step[0].item_id

    # Search step detail
    _model_item.usr_modify(_cond_item)

    # Set return data
    _return.set_str_result("")

    return _return.get_return()


@app.route("/StepDet/usr_search", methods=['POST'])
@allow_cross_domain
def step_det_search():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model_step = StepDetHandle()
    _model_item = ItemHandle()

    _cond_step = _parameter
    _cond_item = {}

    # Search step list
    _steps = _model_step.usr_search(_cond_step)
    _cond_item["id"] = list(_item.item_id for _item in _steps)

    # Search step detail
    _items = _model_item.usr_list_search(_cond_item)

    # Connect data
    _res = _connect(_steps, _items, "item_id")

    # Set return data
    _return.set_arr_result(_res)

    return _return.get_return()


# ---- Share func ---------------------------------------------------------- #
def _connect(p_lists, p_detail, p_flag):

    _res = []

    if 0 == len(p_detail):
        return _res

    for t_step in p_lists:

        _data = t_step.to_json()
        _data.pop("create_time")

        _item_data = dict()
        for t_item in p_detail:

            if str(t_item.id) == _data[p_flag]:

                _item_data = t_item.to_json()
                _item_data.pop("id")

        _data.update(_item_data)

        _res.append(_data)

    return _res
