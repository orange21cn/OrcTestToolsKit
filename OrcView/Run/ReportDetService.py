from OrcLib.LibNet import OrcHttpNewResource


class ReportDetService:

    def __init__(self):

        self.__resource_report = OrcHttpNewResource("Report")

    def get_report_path(self, p_path):

        self.__resource_report.set_path(p_path["path"])
        return self.__resource_report.get()



