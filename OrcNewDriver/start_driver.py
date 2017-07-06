# coding=utf-8
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from OrcDriver import orc_api
from OrcDriver import app
from OrcDriver.DriverApi import DriverListAPI
from OrcLib import get_config
from OrcLib import init_log

reload(sys)
init_log('driver')

configer = get_config("server")

orc_api.add_resource(DriverListAPI, '/api/1.0/Driver', endpoint='Driver')

driver_host = configer.get_option("DRIVER", "ip")
driver_port = configer.get_option("DRIVER", "port")

app.run(host=driver_host, port=driver_port)
