# coding=utf-8
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print os.path.dirname(os.path.dirname(__file__))
from OrcLib import init_log
from OrcLib import get_config

from OrcApi import app
from OrcApi import orc_api

from OrcApi.Run.RunApi import RunDefListAPI
from OrcApi.Run.RunApi import RunDetListAPI
from OrcApi.Run.RunApi import RunListAPI

from OrcApi.RunTime.RunTimeApi import RunTimeListAPI
from OrcApi.RunTime.RunTimeApi import RunTimeAPI

configer = get_config("server")

# Widget
orc_api.add_resource(RunDefListAPI, '/api/1.0/RunDef', endpoint='RunDefs')
orc_api.add_resource(RunDetListAPI, '/api/1.0/RunDet', endpoint='RunDets')
orc_api.add_resource(RunListAPI, '/api/1.0/Run', endpoint='Run')

# RunTime
orc_api.add_resource(RunTimeListAPI, '/api/1.0/RunTime', endpoint='RunTimes')
orc_api.add_resource(RunTimeAPI, '/api/1.0/RunTime/<int:p_id>', endpoint='RunTime')

driver_host = configer.get_option("RUN", "ip")
driver_port = configer.get_option("RUN", "port")

reload(sys)
init_log('run')

app.run(host=driver_host, port=driver_port)