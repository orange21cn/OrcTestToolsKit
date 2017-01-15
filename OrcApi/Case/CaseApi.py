# coding=utf-8
from OrcLib.LibNet import orc_api
from OrcLib.LibNet import OrcParameter
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
        self._logger.info("Move step %s, parameter is: %s" % (p_para, p_id))

        if "up" == p_para["cmd"]:
            return self._business.bus_up(p_id)

        elif "down" == p_para["cmd"]:
            return self._business.bus_down(p_id)

        else:
            self._logger.error("Wrong parameter: %s" % p_para)
            return False
