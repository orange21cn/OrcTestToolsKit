# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibApi import connect_list
from OrcView.Lib.LibView import ResourceCheck


class CaseDefService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_case_def = OrcResource("CaseDef")
        self.__resource_run_def = OrcResource("RunDef")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_case_def.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增用例"):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增用例")

        return dict(id=result.data["id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_case_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除用例"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除用例")

        return result.status

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        result = self.__resource_case_def.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新用例"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新用例")

        return result.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        cond = dict(type="all")
        cond.update(p_cond)
        result = self.__resource_case_def.get(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询用例"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询用例")

        return result.data

    def add_to_run(self, p_id):
        """
        加入运行
        :param p_id:
        :return:
        """
        cond = dict(id=p_id, run_def_type="CASE")
        result = self.__resource_run_def.post(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"添加至运行"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"添加至运行")

        return True


class CaseDetService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_case_det = OrcResource("CaseDet")
        self.__resource_step = OrcResource("StepDef")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        # 增加步骤
        step_info = p_data["step"]
        step_det = self.__resource_step.post(parameter=step_info)

        # 检查结果
        if not ResourceCheck.result_status(step_det, u"新增步骤"):
            return dict()

        # 增加 case
        case_info = p_data["case_det"]
        case_info["step_id"] = step_det.data["id"]

        case_det = self.__resource_case_det.post(parameter=case_info)

        # 检查结果
        if not ResourceCheck.result_status(case_det, u"新增用例步骤"):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增用例步骤")

        return dict(case_id=case_det.data["case_id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_case_det.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除用例步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除用例步骤")

        return result.status

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        # 获取 step id
        case_det_info = self.__resource_case_det.get(path=p_data["id"])

        # 检查结果
        if not ResourceCheck.result_status(case_det_info, u"获取步骤ID"):
            return False

        # 更新数据
        data = p_data.copy()
        data["id"] = case_det_info.data["step_id"]

        step_info = self.__resource_step.put(path=data["id"], parameter=data)

        # 检查结果
        if not ResourceCheck.result_status(step_info, u"更新步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新步骤")

        return step_info.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        # 查询 case_det 列表
        case_det_info = self.__resource_case_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(case_det_info, u"查询步骤"):
            return list()

        # 查询 step id 列表
        step_id_list = [item["step_id"] for item in case_det_info.data]

        # 查询 step_def 列表
        step_def_info = self.__resource_step.get(parameter=dict(id=step_id_list))

        # 检查结果
        if not ResourceCheck.result_status(step_def_info, u"查询步骤"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询步骤")

        # 连接数据
        return connect_list(case_det_info.data, step_def_info.data, "step_id")

    def usr_up(self, p_id):
        """
        上移
        :param p_id:
        :return:
        """
        result = self.__resource_case_det.post(path=p_id, parameter=dict(cmd="up"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"上移步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"上移步骤")

        return result.status

    def usr_down(self, p_id):
        """
        下移
        :param p_id:
        :return:
        """
        result = self.__resource_case_det.post(path=p_id, parameter=dict(cmd="down"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"下移步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"下移步骤")

        return result.status
