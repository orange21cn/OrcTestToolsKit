# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibApi import connect_list

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTable import ModelTable


class StepModel(ModelTable):

    def __init__(self, p_def='Step'):

        ModelTable.__init__(self, p_def)

        self.__logger = LogClient()

        self.__resource_case_det = OrcResource("CaseDet")
        self.__resource_step_def = OrcResource("StepDef")

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        # 增加步骤
        step_info = p_data["step"]
        step_det = self.__resource_step_def.post(parameter=step_info)

        # 检查结果
        if not ResourceCheck.result_status(step_det, u"新增步骤", self.__logger):
            return dict()

        # 增加 case
        case_info = p_data["case_det"]
        case_info["step_id"] = step_det.data["id"]

        case_det = self.__resource_case_det.post(parameter=case_info)

        # 检查结果
        if not ResourceCheck.result_status(case_det, u"新增用例步骤", self.__logger):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增用例步骤", self.__logger)

        return dict(case_id=case_det.data["case_id"])

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_case_det.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除用例步骤", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除用例步骤", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        # 获取 step id
        case_det_info = self.__resource_case_det.get(path=p_data["id"])

        # 检查结果
        if not ResourceCheck.result_status(case_det_info, u"获取步骤ID", self.__logger):
            return False

        # 更新数据
        data = p_data.copy()
        data["id"] = case_det_info.data["step_id"]

        step_info = self.__resource_step_def.put(path=data["id"], parameter=data)

        # 检查结果
        if not ResourceCheck.result_status(step_info, u"更新步骤", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新步骤", self.__logger)

        return step_info.status

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        # 查询 case_det 列表
        case_det_info = self.__resource_case_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(case_det_info, u"查询步骤", self.__logger):
            return list()

        # 查询 step id 列表
        step_id_list = [item["step_id"] for item in case_det_info.data]

        # 查询 step_def 列表
        step_def_info = self.__resource_step_def.get(parameter=dict(id=step_id_list))

        # 检查结果
        if not ResourceCheck.result_status(step_def_info, u"查询步骤", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询步骤", self.__logger)

        # 连接数据
        return connect_list(case_det_info.data, step_def_info.data, "step_id")

    def service_up(self, p_id):
        """
        上移
        :param p_id:
        :return:
        """
        result = self.__resource_case_det.post(path=p_id, parameter=dict(cmd="up"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"上移步骤", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"上移步骤", self.__logger)

        return result.status

    def service_down(self, p_id):
        """
        下移
        :param p_id:
        :return:
        """
        result = self.__resource_case_det.post(path=p_id, parameter=dict(cmd="down"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"下移步骤", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"下移步骤", self.__logger)

        return result.status
