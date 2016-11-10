from OrcLib.LibNet import get_config
from OrcDriver.Web.WebDriver import DriverSelenium

configer = get_config("network")

driver_host = configer.get_option("SERVER_WEB_001", "ip")
driver_port = configer.get_option("SERVER_WEB_001", "port")

_test = DriverSelenium(driver_host, driver_port)
_test.start()
