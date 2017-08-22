# coding=utf-8
from OrcLib.LibApi import OrcListAPI
from OrcLib.LibApi import OrcAPI

from .DataBaseBus import DataBaseBus


class DataBaseListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "data_base", DataBaseBus)

    def dispatch_request(self, *args, **kwargs):
        return super(DataBaseListAPI, self).dispatch_request(*args, **kwargs)
