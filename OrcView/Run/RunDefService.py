# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib import get_config
from OrcView.Lib.LibView import ResourceCheck


class RunDefService:

    def __init__(self):

        self.__res_run_def = OrcResource("RunDef")
        self.__res_run = OrcResource("Run")
        self.__configer = get_config("server")

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

        result = self.__res_run_def.post(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增测试项"):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增测试项")

        return dict()

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__res_run_def.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询测试项"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询测试项")

        return result.data

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__res_run_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除测试项"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除测试项")

        return result.status

    def usr_run(self, p_pid, p_id):
        """
        执行, pid 目录id, id 条目 id, 发送 ip/port 用于回调
        :param p_pid:
        :param p_id:
        :return:
        """
        pro_ip = self.__configer.get_option("VIEW", "ip")
        pro_port = self.__configer.get_option("VIEW", "port")
        result = self.__res_run.put(parameter=dict(pid=p_pid, id=p_id, ip=pro_ip, port=pro_port))

        # 检查结果
        if not ResourceCheck.result_status(result, u"运行测试项"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"运行测试项")

        return result.status
