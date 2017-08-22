# coding=utf-8
import os
from RunCore import RunCore
from OrcLib import get_config


class ReportDetMod:

    def __init__(self):

        self._core = RunCore()

        self._configer = get_config()
        self._home = self._configer.get_option("RUN", "home")

    def usr_search(self, p_path):
        """
        :param p_path:
        :type p_path: dict
        :return:
        """
        pass

    def usr_get_report(self, p_id, p_time):
        """

        :param p_id:
        :param p_time:
        :return:
        """
        report_path = "%s/%s/%s" % (self._home, p_id, p_time)
        report_file = "%s/report.html" % report_path
        result_file = "%s/default.res" % report_path

        # 生成报告
        if not os.path.exists(report_file):
            return self.__create_report(result_file, report_file)
        else:
            return "No result"

    def __create_report(self, p_res, p_rpt):
        """

        :param p_res:
        :param p_rpt:
        :return:
        """
        from lxml import etree

        template_path = "%s/report/basic/basic.xml" % self._configer.get_option("TEMPLATE", "template_root_path")

        with open(p_res, "r") as result_file, open(template_path, "r") as template_file:
            result_content = etree.XML(result_file.read())
            template_xslt = etree.XSLT(etree.XML(template_file.read()))
            report_content = template_xslt(result_content)

        return str(report_content)
