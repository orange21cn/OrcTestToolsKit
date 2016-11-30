# coding=utf-8
from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResult
from ReportDetModel import ReportDetModel


class ReportDetAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("api.report.det")
        self.__model = ReportDetModel()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    def get(self, p_id, p_time):
        """
        Search
        :param p_time:
        :param p_id:
        :return:
        """
        print p_id
        print p_time
        _parameter = dict(id=p_id)
        _return = OrcResult()

        _value = "<html><head></head><body><h1>Hello</h1></body></html>"

        return self.__model.usr_get_report(p_id, p_time)
