# coding=utf-8
from OrcLib.LibApi import OrcListAPI
from OrcLib.LibApi import OrcAPI

from WidgetBus import WidgetDefBus
from WidgetBus import WidgetDetBus


class WidgetDefListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "widget_def", WidgetDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class WidgetDefAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "widget_def", WidgetDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)


class WidgetDetListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "widget_det", WidgetDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class WidgetDetAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "widget_det", WidgetDetBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)
