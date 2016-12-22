# coding=utf-8
from OrcLib.LibApi import OrcBaseAPI
from OrcLib.LibApi import OrcListAPI
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api

from RunDefBus import RunDefBus
from RunDetMod import RunDetMod
from RunCore import RunCore


class RunDefListAPI(OrcListAPI):

    def __init__(self):

        OrcListAPI.__init__(self, "run_def", RunDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class RunDetListAPI(OrcBaseAPI):

    def __init__(self):

        OrcBaseAPI.__init__(self, "run_det", RunDetMod)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcBaseAPI, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self._logger.info("Add run time, parameter is: %s" % parameter)

        return self._business.usr_search(parameter)


class RunAPI(OrcBaseAPI):

    def __init__(self):

        OrcBaseAPI.__init__(self, "run", RunCore)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcBaseAPI, self).dispatch_request(*args, **kwargs)

    @orc_api
    def put(self):
        """
        start
        """
        parameter = OrcParameter.receive_para()

        self._logger.info("Run, parameter is: %s" % parameter)

        return self._business.run_start(parameter)
