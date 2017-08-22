# coding=utf-8
from OrcLib.LibApi import OrcBaseAPI
from OrcLib.LibApi import OrcListAPI
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api

from RunDefBus import RunDefBus
from RunDetMod import RunDetMod
from RunCore import RunCore


class RunDefListAPI(OrcListAPI):
    """

    """
    def __init__(self):

        OrcListAPI.__init__(self, "run_def", RunDefBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class RunDetListAPI(OrcBaseAPI):
    """

    """
    def __init__(self):

        OrcBaseAPI.__init__(self, "run_det", RunDetMod)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcBaseAPI, self).dispatch_request(*args, **kwargs)

    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.api_get(parameter)

    @orc_api
    def api_get(self, p_para):
        self._logger.info("Add run time, parameter is: %s" % p_para)
        return self._business.usr_search(p_para)


class RunListAPI(OrcBaseAPI):
    """

    """
    def __init__(self):

        OrcBaseAPI.__init__(self, "run", RunCore)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcBaseAPI, self).dispatch_request(*args, **kwargs)

    def put(self):
        """
        start
        """
        parameter = OrcParameter.receive_para()
        return self.api_put(parameter)

    @orc_api
    def api_put(self, p_para):
        self._logger.info("Run, parameter is: %s" % p_para)
        return self._business.start(p_para)

    def delete(self):
        """
        start
        """
        return self.api_put()

    @orc_api
    def api_delete(self):

        self._logger.info('Stop')
        return self._business.stop()

    def get(self):
        """
        获取状态
        """
        return self.api_put()

    @orc_api
    def api_get(self):

        self._logger.info("Get run status.")
        return self._business.get_status()
