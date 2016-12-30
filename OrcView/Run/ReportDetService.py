from OrcLib.LibNet import OrcHttpResource


class ReportDetService:

    def __init__(self):

        self.__resource_report = OrcHttpResource("Report")

    def get_report_path(self, p_path):

        self.__resource_report.set_path(p_path["path"])
        res = self.__resource_report.get()

        return res



