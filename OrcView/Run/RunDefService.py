from OrcLib.LibNet import OrcHttpResource


class RunDefService:

    def __init__(self):

        self.__res_run_def = OrcHttpResource("RunDef")
        self.__res_run = OrcHttpResource("Run")

    def usr_add(self, p_cond):
        """
        :param p_cond: {id, run_def_type, result}
        :return:
        """
        if "pid" not in p_cond:
            return dict()

        cond = dict(
            id=p_cond["pid"],
            run_def_type=p_cond["run_def_type"],
            result=True)

        self.__res_run_def.set_path(cond["id"])
        res = self.__res_run_def.post(cond)

        return dict(id=res)

    def usr_search(self, p_cond):
        return self.__res_run_def.get(p_cond)

    def usr_delete(self, p_list):
        self.__res_run_def.delete(p_list)

    def usr_run(self, p_pid, p_id):

        self.__res_run.put(dict(pid=p_pid, id=p_id))
