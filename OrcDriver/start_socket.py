from OrcDriver.Web.WebServer import DriverSelenium

_test = DriverSelenium("localhost", 6001)
_test.start()