# coding=utf-8
import sys

from OrcApi import app
from OrcApi.Batch import api
from OrcApi.Case import api
from OrcApi.Data import api
from OrcApi.Driver.Web import api
from OrcApi.Lib import api
from OrcLib import init_log

reload(sys)
init_log()

app.run(host='localhost')
