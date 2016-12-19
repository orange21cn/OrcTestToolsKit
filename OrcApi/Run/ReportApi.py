# coding=utf-8
from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_api
from ReportDetModel import ReportDetModel


class ReportDetAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.report.api.det")
        self.__model = ReportDetModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id, p_time):
        """
        Search
        :param p_time:
        :param p_id:
        :return:
        """
        self.__logger.info("Get report, parameter is: %s, %s" % (p_id, p_time))

        return self.__model.usr_get_report(p_id, p_time)
