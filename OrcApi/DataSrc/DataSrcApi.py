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
        return super(OrcListAPI, self).dispatch_request(*args, **kwargs)


class DataSrcAPI(OrcAPI):

    def __init__(self):

        OrcAPI.__init__(self, "data_src", DataSrcBus)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcAPI, self).dispatch_request(*args, **kwargs)

    def post(self, p_id):
        """
        执行 sql
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()
        return self.api_post(p_id, parameter)

    @orc_api
    def api_post(self, p_id, p_cmd):
        """
        Search
        :param p_id:
        :param p_cmd:
        :return:
        """
        self._logger.info("Launch command: %s" % p_cmd)

        return self._business.bus_post(p_id, p_cmd)