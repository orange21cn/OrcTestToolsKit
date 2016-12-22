# coding=utf-8
from OrcLib.LibApi import OrcAPI
from OrcLib.LibApi import OrcListAPI

from BatchBus import BatchDefBus
from BatchBus import BatchDetBus


class BatchDefListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "batch_def", BatchDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class BatchDefAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "batch_def", BatchDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)


class BatchDetListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "batch_det", BatchDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class BatchDetAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "batch_det", BatchDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)
