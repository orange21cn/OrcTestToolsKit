# coding=utf-8
from OrcLib import get_config
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTree import ModelTree


class RunDefModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self, 'RunDef')

        self.__logger = LogClient()

        self.__resource_run_def = OrcResource("RunDef")
        self.__resource_run = OrcResource("Run")
        self.__configer = get_config("server")

    def service_add(self, p_cond):
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

        result = self.__resource_run_def.post(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增测试项", self.__logger):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增测试项", self.__logger)

        return dict()

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource_run_def.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询测试项", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询测试项", self.__logger)

        return result.data

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        print p_list
        result = self.__resource_run_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除测试项", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除测试项", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        pass

    def service_run(self, p_pid, p_id):
        """
        执行, pid 目录id, id 条目 id, 发送 ip/port 用于回调
        :param p_pid:
        :param p_id:
        :return:
        """
        pro_ip = self.__configer.get_option("VIEW", "ip")
        pro_port = self.__configer.get_option("VIEW", "port")
        result = self.__resource_run.put(parameter=dict(pid=p_pid, id=p_id, ip=pro_ip, port=pro_port))

        # 检查结果
        if not ResourceCheck.result_status(result, u"运行测试项", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"运行测试项", self.__logger)

        return

    def service_stop(self):
        """
        停止
        :return:
        """
        self.__resource_run.delete()

    # def service_update_status(self):
    #     """
    #     获取状态
    #     :return:
    #     """
    #     result = self.__resource_run.get()
    #
    #     # 检查结果
    #     if not ResourceCheck.result_status(result, u"获取运行状态", self.__logger):
    #         return False
    #
    #     # 打印成功信息
    #     ResourceCheck.result_success(u"获取运行状态", self.__logger)
    #
    #     return result.data
