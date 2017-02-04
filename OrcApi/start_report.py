# coding=utf-8
import sys

from flask import make_response

from OrcLib import init_log
from OrcLib import get_config
from OrcApi import app
from OrcApi import orc_api
from OrcApi.Run.ReportApi import ReportAPI

configer = get_config("server")


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@orc_api.representation("text/html")
def out_html(data, code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


# Widget
orc_api.add_resource(ReportAPI, '/api/1.0/Report/<string:p_id>/<string:p_time>', endpoint='Report')

driver_host = configer.get_option("REPORT", "ip")
driver_port = configer.get_option("REPORT", "port")

reload(sys)
init_log()

app.run(host=driver_host, port=driver_port)
