# coding=utf-8
import sys

from OrcLib import init_log

from OrcApi import app
from OrcApi import orc_api

from OrcApi.Run.RunApi import RunDefListAPI
from OrcApi.Run.RunApi import RunDefAPI
from OrcApi.Run.RunApi import RunDetListAPI
from OrcApi.Run.RunApi import RunAPI


# Widget
orc_api.add_resource(RunDefListAPI, '/api/1.0/RunDef', endpoint='RunDefs')
orc_api.add_resource(RunDefAPI, '/api/1.0/RunDef/<int:p_id>', endpoint='RunDef')
orc_api.add_resource(RunDetListAPI, '/api/1.0/RunDet', endpoint='RunDets')
orc_api.add_resource(RunAPI, '/api/1.0/Run', endpoint='Run')

reload(sys)
init_log()

app.run(host='localhost', port=5004)
