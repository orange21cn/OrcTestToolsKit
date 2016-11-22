# coding=utf-8
import os
from RunCore import RunCore
from OrcLib import get_config


class ReportDetModel:

    def __init__(self):

        self.__core = RunCore()
        self.__home = self.__core.get_home()
        self.__configer = get_config()

    def usr_search(self, p_path):
        """
        :param p_path:
        :type p_path: dict
        :return:
        """
        res_file = "%s/%s" % (self.__home, p_path["path"])

        if not os.path.exists(res_file):
            return

        self.__core.load_list(res_file)

        return self.__core.list

    def usr_get_report(self, p_id, p_time):

        report_path = "%s/%s/%s" % (self.__core.get_home(), p_id, p_time)
        report_file = "%s/report.html" % report_path
        result_file = "%s/default.res" % report_path

        # 生成报告
        if not os.path.exists(report_file):
            return self.__create_report(result_file, report_file)
        else:
            return "No result"

        # 发送报告

    def __create_report(self, p_res, p_rpt):

        from lxml import etree

        result_file = open(p_res, "r")
        test01 = etree.XML(result_file.read())
        result_file.close()

        test02 = "%s/report/default/default.xml" % self.__configer.get_option("TEMPLATE", "template_root_path")
        test03 = open(test02, "r")
        test05 = etree.XML(test03.read())
        test04 = etree.XSLT(test05)
        test03.close()

        abc = test04(test01)

        return str(abc)