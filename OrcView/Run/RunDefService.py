# coding=utf-8
from OrcLib.LibNet import OrcHttpNewResource


class RunDefService:

    def __init__(self):

        self.__res_run_def = OrcHttpNewResource("RunDef")
        self.__res_run = OrcHttpNewResource("Run")

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

        self.__res_run_def.post(cond)

        return dict()

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return self.__res_run_def.get(p_cond)

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        self.__res_run_def.delete(p_list)

    def usr_run(self, p_pid, p_id):
        """
        执行
        :param p_pid:
        :param p_id:
        :return:
        """
        self.__res_run.put(dict(pid=p_pid, id=p_id))
