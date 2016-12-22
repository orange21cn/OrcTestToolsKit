# coding=utf-8
from OrcLib.LibApi import OrcListAPI
from OrcLib.LibApi import OrcAPI

from StepBus import StepDefBus
from StepBus import StepDetBus


class StepDefListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "step_def", StepDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request()


class StepDefAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "step_def", StepDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)


class StepDetListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "step_det", StepDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class StepDetAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "step_det", StepDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)
