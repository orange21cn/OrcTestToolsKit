# coding=utf-8
from OrcLib.LibApi import OrcListAPI
from OrcLib.LibApi import OrcAPI
from OrcLib.LibApi import orc_api
from OrcLib.LibApi import OrcParameter

from .DataSrcBus import DataSrcBus


class DataSrcListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "data_src", DataSrcBus)

    def dispatch_request(self, *args, **kwargs):
        return super(DataSrcListAPI, self).dispatch_request(*args, **kwargs)


class DataSrcAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "data_src", DataSrcBus)

    def dispatch_request(self, *args, **kwargs):
        return super(DataSrcAPI, self).dispatch_request(*args, **kwargs)
