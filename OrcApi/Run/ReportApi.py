# coding=utf-8
from OrcLib.LibApi import OrcBaseAPI
from OrcLib.LibNet import orc_api

from ReportDetMod import ReportDetMod


class ReportAPI(OrcBaseAPI):

    def __init__(self):

        OrcBaseAPI.__init__(self, "report", ReportDetMod)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcBaseAPI, self).dispatch_request(*args, **kwargs)

    # @orc_api
    def get(self, p_id, p_time):
        """
        Search
        :param p_time:
        :param p_id:
        :return:
        """
        self._logger.info("Get report, parameter is: %s, %s" % (p_id, p_time))

        return self._business.usr_get_report(p_id, p_time)


class ResourceAPI(OrcBaseAPI):

    def __init__(self):

        OrcBaseAPI.__init__(self, 'resource', ReportDetMod)

    def dispatch_request(self, *args, **kwargs):
        return super(OrcBaseAPI, self).dispatch_request(*args, **kwargs)

    def get(self, p_file):

        return self._business.usr_get_resource(p_file)
