# coding=utf-8
from OrcLib.LibApi import OrcListAPI
from OrcLib.LibApi import OrcAPI

from PageBus import PageDefBus
from PageBus import PageDetBus


class PageDefListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "page_def", PageDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class PageDefAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "page_def", PageDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)


class PageDetListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "page_det", PageDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class PageDetAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "page_det", PageDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)
