from OrcLib.LibNet import OrcHttpResource


class RunDefService:

    def __init__(self):

        self.__res_run_def = OrcHttpResource("RunDef")

    def usr_search(self, p_cond):
        return self.__res_run_def.get()

    def usr_delete(self, p_list):
        self.__res_run_def.delete(p_list)

    def usr_run(self):
        pass
