# coding=utf-8
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import make_response
from flask import redirect
from flask import url_for

from OrcLib import init_log
from OrcLib import get_config
from OrcApi import app
from OrcApi import orc_api
from OrcApi.Run.ReportApi import ReportAPI
from OrcApi.Run.ReportApi import ResourceAPI

configer = get_config("server")


# @app.after_request
# def after_request(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response
#
# @orc_api.representation("text/javascript")
# def out_html(data, code, headers=None):
#     resp = make_response(data, code)
#     resp.headers.extend(headers or {})
#     return resp
#
# # Resource
# orc_api.add_resource(ResourceAPI, '/api/1.0/Resource/<string:p_file>', endpoint='Resource')
#
driver_host = configer.get_option("REPORT", "ip")
driver_port = configer.get_option("REPORT", "port")
#
# reload(sys)
# # init_log('report')


@app.route('/api/1.0/Resource/<string:p_file>')
def index(p_file):
    return redirect(url_for('static', filename=p_file))

app.run(host=driver_host, port=5006)
