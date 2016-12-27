# coding=utf-8
import sys

from OrcDriver import orc_api
from OrcDriver import app
from OrcDriver.DriverApi import DriverAPI
from OrcLib import get_config
from OrcLib import init_log

reload(sys)
init_log()

configer = get_config("server")

orc_api.add_resource(DriverAPI, '/api/1.0/Driver', endpoint='Driver')

driver_host = configer.get_option("DRIVER", "ip")
driver_port = configer.get_option("DRIVER", "port")

app.run(host=driver_host, port=driver_port)
