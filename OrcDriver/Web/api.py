# -*- coding: utf-8 -*-
import logging
from OrcLib.LibNet import OrcReturn
from OrcLib.LibNet import allow_cross_domain
from OrcLib.LibNet import orc_get_parameter
from OrcLib.LibNet import OrcInvoke
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

    print _parameter
    import json

    _value = OrcInvoke.socket("localhost", 6001, json.dumps(_parameter))

    _return.set_str_result(_value)

    return _return.get_return()
