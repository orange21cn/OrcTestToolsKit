# -*- coding: utf-8 -*-
from OrcLib.LibNet import OrcReturn
from OrcLib.LibNet import allow_cross_domain
from OrcLib.LibNet import orc_get_parameter
from OrcApi.Lib.Dictionory import DictHandle
from OrcApi import app


@app.route("/Lib/usr_get_dict_text", methods=['POST'])
@allow_cross_domain
def lib_get_dict_text():
    """
    request: {id:..,case_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = DictHandle()

    _value = _model.get_dict_text(_parameter)

    _return.set_str_result(_value)

    return _return.get_return()