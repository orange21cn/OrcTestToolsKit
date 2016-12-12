# coding=utf-8
from OrcLib.LibNet import OrcHttpNewResource


class RunDetService():

    def __init__(self):

        self.__resource_run_det = OrcHttpNewResource("RunDet")
        self.__resource_run = OrcHttpNewResource("Run")

    def usr_search(self, p_path):

        res = self.__resource_run_det.get(p_path)

        return res

    def usr_run(self, p_path):
        self.__resource_run.put(p_path)
