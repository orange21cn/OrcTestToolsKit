# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibApi import connect_list

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTable import ModelTable


class BatchDetModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self, 'BatchDet')

        self.__logger = LogClient()

        self.__resource_batch_det = OrcResource("BatchDet")
        self.__resource_case_def = OrcResource("CaseDef")

    def service_add(self, p_data):
        """
        增加,将多条记录转换为单条
        :param p_data:
        :return:
        """
        batch_id = p_data["batch_id"]

        for _case_id in p_data["case"]:

            result = self.__resource_batch_det.post(parameter=dict(batch_id=batch_id, case_id=_case_id))

            # 检查结果
            if not ResourceCheck.result_status(result, u"添加计划用例", self.__logger):
                return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"添加计划用例", self.__logger)

        return dict(batch_id=batch_id)

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_batch_det.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除计划用例", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除计划用例", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        result = self.__resource_batch_det.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新计划用例", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新计划用例", self.__logger)

        return result.status

    def service_search(self, p_cond):
        """
        查询,查询batch及case并连接数据
        :param p_cond:
        :return:
        """
        # 查询 batch_det 列表
        batch_det_info = self.__resource_batch_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(batch_det_info, u"查询计划用例列表", self.__logger):
            return list()

        # case_det id 列表
        case_def_id_list = [batch_det["case_id"] for batch_det in batch_det_info.data]

        # case_def 列表
        case_info = self.__resource_case_def.get(parameter=dict(id=case_def_id_list))

        # 检查结果
        if not ResourceCheck.result_status(batch_det_info, u"查询用例信息列表", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询用例信息列表", self.__logger)

        # 连接 list 并返回
        return connect_list(batch_det_info.data, case_info.data, "case_id")