# coding=utf-8
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from OrcLib import get_config
from OrcLib import init_log
from OrcApi.OrcDriver.OrcDriver import OrcDriver

configer = get_config("server")


init_log('driver')

_test = OrcDriver()
_test.start()

