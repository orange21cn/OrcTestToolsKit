# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck


class ReportDetService:

    def __init__(self):

        self.__resource_report = OrcResource("Report", mode="HTML")

    def get_report_path(self, p_path):

        result = self.__resource_report.get(path=p_path["path"])

        return "%s/%s" % (self.__resource_report._url, p_path["path"])




