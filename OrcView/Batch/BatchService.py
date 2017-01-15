# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibApi import connect_list
from OrcView.Lib.LibView import ResourceCheck


class BatchDefService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_batch_def = OrcResource("BatchDef")
        self.__resource_run_def = OrcResource("RunDef")

    def usr_add(self, p_data):
        """
        增加
        :param p_data:
        :return:
        """
        result = self.__resource_batch_def.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"新增计划"):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"新增计划")

        return dict(id=result.data["id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_batch_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除计划"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"新增计划")

        return result.status

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        result = self.__resource_batch_def.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新计划"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新计划")

        return result.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        cond = dict(type="all")
        cond.update(p_cond)

        result = self.__resource_batch_def.get(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询计划"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询计划")

        return result.data

    def add_to_run(self, p_id):
        """
        加入运行列表
        :param p_id:
        :return:
        """
        cond = dict(id=p_id, run_def_type="BATCH")
        result = self.__resource_run_def.post(parameter=cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"添加至运行"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"添加至运行")

        return True


class BatchDetService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_batch_det = OrcResource("BatchDet")
        self.__resource_case_def = OrcResource("CaseDef")

    def usr_add(self, p_data):
        """
        增加,将多条记录转换为单条
        :param p_data:
        :return:
        """
        batch_id = p_data["batch_id"]

        for _case_id in p_data["case"]:

            result = self.__resource_batch_det.post(parameter=dict(batch_id=batch_id, case_id=_case_id))

            # 检查结果
            if not ResourceCheck.result_status(result, u"添加计划用例"):
                return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"添加计划用例")

        return dict(batch_id=batch_id)

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_batch_det.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除计划用例"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除计划用例")

        return result.status

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        result = self.__resource_batch_det.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新计划用例"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新计划用例")

        return result.status

    def usr_search(self, p_cond):
        """
        查询,查询batch及case并连接数据
        :param p_cond:
        :return:
        """
        # 查询 batch_det 列表
        batch_det_info = self.__resource_batch_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(batch_det_info, u"查询计划用例列表"):
            return list()

        # case_det id 列表
        case_def_id_list = [batch_det["case_id"] for batch_det in batch_det_info.data]

        # case_def 列表
        case_info = self.__resource_case_def.get(parameter=dict(id=case_def_id_list))

        # 检查结果
        if not ResourceCheck.result_status(batch_det_info, u"查询用例信息列表"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询用例信息列表")

        # 连接 list 并返回
        return connect_list(batch_det_info.data, case_info.data, "case_id")
