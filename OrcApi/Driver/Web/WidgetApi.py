# coding=utf-8
from OrcLib.LibNet import orc_api
from OrcLib.LibNet import OrcParameter
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

    def post(self, p_id):
        """
        POST
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.api_post(p_id, parameter)

    @orc_api
    def api_post(self, p_id, p_para):
        """
        POST
        :param p_id:
        :return:
        """
        self._logger.info("Move attribute %s, parameter is: %s" % (p_para, p_id))

        if "up" == p_para["cmd"]:
            return self._business.bus_up(p_id)

        elif "down" == p_para["cmd"]:
            return self._business.bus_down(p_id)

        else:
            self._logger.error("Wrong parameter: %s" % p_para)
            return False
