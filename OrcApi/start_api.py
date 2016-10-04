# coding=utf-8
import sys

from OrcApi import app
from OrcApi import orc_api

from OrcApi.Batch import api
from OrcApi.Case import api
from OrcApi.Data import api
from OrcApi.Driver.Web import api
from OrcApi.Lib import api
from OrcLib import init_log
from OrcApi.Driver.Web.WindowApi import WindowsListAPI
from OrcApi.Driver.Web.WindowApi import WindowsAPI


orc_api.add_resource(WindowsListAPI, '/api/1.0/windows', endpoint='windows')
orc_api.add_resource(WindowsAPI, '/api/1.0/windows/<int:p_id>', endpoint='window')

reload(sys)
init_log()

app.run(host='localhost')
