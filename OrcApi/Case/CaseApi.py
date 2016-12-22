# coding=utf-8
from OrcLib.LibApi import OrcListAPI
from OrcLib.LibApi import OrcAPI

from CaseBus import CaseDefBus
from CaseBus import CaseDetBus


class CaseDefListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "case_def", CaseDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class CaseDefAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "case_def", CaseDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)


class CaseDetListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "case_det", CaseDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class CaseDetAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "case_det", CaseDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)
