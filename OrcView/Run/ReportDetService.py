# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcView.Lib.LibView import ResourceCheck


class ReportDetService:

    def __init__(self):

        self.__resource_report = OrcResource("Report")

    def get_report_path(self, p_path):

        result = self.__resource_report.get(path=p_path["path"])

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取报告路径"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"获取报告路径")

        return result.data



