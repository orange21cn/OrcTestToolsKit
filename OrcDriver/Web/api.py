# -*- coding: utf-8 -*-
import logging
from OrcLib.LibNet import OrcReturn
from OrcLib.LibNet import allow_cross_domain
from OrcLib.LibNet import orc_get_parameter
from OrcDriver.Web.WebServer import DriverSelenium

from OrcDriver import app


api_batch_log = logging.getLogger("api")


# ---- Batch definition ---------------------------------------------------------- #
@app.route("/WebServer/run", methods=['POST'])
@allow_cross_domain
def api_web_run():
    """
    request: {id:..,batch_no:....}
    :return:
    """
    _parameter = orc_get_parameter()
    _return = OrcReturn()

    _model = DriverSelenium()
    _value = _model.get_test()

    _return.set_db_result(_value)

    return _return.get_return()
