# coding=utf-8
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibApi import connect_list


class CaseDefService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_case_def = OrcHttpResource("CaseDef")
        self.__resource_run_def = OrcHttpResource("RunDef")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        case_def_data = self.__resource_case_def.post(p_data)
        return dict(id=case_def_data["id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        return self.__resource_case_def.delete(p_list)

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        self.__resource_case_def.set_path(p_data["id"])
        return self.__resource_case_def.put(p_data)

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        cond = dict(type="all")
        cond.update(p_cond)
        return self.__resource_case_def.get(cond)

    def add_to_run(self, p_id):
        """
        加入运行
        :param p_id:
        :return:
        """
        cond = dict(id=p_id, run_def_type="CASE")
        self.__resource_run_def.post(cond)


class CaseDetService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_case_det = OrcHttpResource("CaseDet")
        self.__resource_step = OrcHttpResource("StepDef")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        # 增加步骤
        step_info = p_data["step"]
        step_det = self.__resource_step.post(step_info)

        # 增加 case
        case_info = p_data["case_det"]
        case_info["step_id"] = step_det["id"]

        case_det = self.__resource_case_det.post(case_info)

        return dict(case_id=case_det["case_id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        return self.__resource_case_det.delete(p_list)

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        # 获取 step id
        self.__resource_case_det.set_path(p_data["id"])
        step_id = self.__resource_case_det.get()["step_id"]

        # 更新数据
        data = p_data.copy()
        data["id"] = step_id
        self.__resource_step.set_path(step_id)

        return self.__resource_step.put(data)

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        # 查询 case_det 列表
        case_det_list = self.__resource_case_det.get(p_cond)

        # 查询 step id 列表
        step_id_list = [item["step_id"] for item in case_det_list]

        # 查询 step_def 列表
        step_def_list = self.__resource_step.get(dict(id=step_id_list))

        # 连接数据
        return connect_list(case_det_list, step_def_list, "step_id")
