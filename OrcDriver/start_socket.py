# coding=utf-8
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from OrcLib import get_config
from OrcLib import init_log
from OrcDriver.Web.WebDriver import DriverSelenium

configer = get_config("server")

driver_host = configer.get_option("SERVER_WEB_001", "ip")
driver_port = configer.get_option("SERVER_WEB_001", "port")

init_log('socket')

_test = DriverSelenium(driver_host, driver_port)
_test.start()
