# coding=utf-8
import sys
from OrcDriver import app
from OrcDriver.Web import api
from OrcLib import init_log

reload(sys)
init_log()

app.run(host='localhost', port=5002)


