# coding=utf-8
from OrcLib.LibNet import OrcHttpResource


class RunDetService():

    def __init__(self):

        self.__resource_run_det = OrcHttpResource("RunDet")

    def usr_search(self, p_path):

        res = self.__resource_run_det.get(p_path)

        return res
