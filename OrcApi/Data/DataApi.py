# coding=utf-8
from OrcLib.LibApi import OrcListAPI
from OrcLib.LibApi import OrcAPI

from DataBus import DataBus


class DataListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "data", DataBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class DataAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "data", DataBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)
