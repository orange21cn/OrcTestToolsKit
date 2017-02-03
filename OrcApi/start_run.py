# coding=utf-8
import sys

from OrcLib import init_log
from OrcLib import get_config

from OrcApi import app
from OrcApi import orc_api

from OrcApi.Run.RunApi import RunDefListAPI
from OrcApi.Run.RunApi import RunDetListAPI
from OrcApi.Run.RunApi import RunListAPI

configer = get_config("server")


# Widget
orc_api.add_resource(RunDefListAPI, '/api/1.0/RunDef', endpoint='RunDefs')
orc_api.add_resource(RunDetListAPI, '/api/1.0/RunDet', endpoint='RunDets')
orc_api.add_resource(RunListAPI, '/api/1.0/Run', endpoint='Run')

driver_host = configer.get_option("RUN", "ip")
driver_port = configer.get_option("RUN", "port")

reload(sys)
init_log()

app.run(host=driver_host, port=driver_port)