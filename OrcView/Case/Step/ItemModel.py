# coding=utf-8
import json

from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibApi import connect_list

from OrcView.Lib.LibView import operate_to_str
from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTable import StaticModelTable


class ItemModel(StaticModelTable):

    def __init__(self, p_def):

        StaticModelTable.__init__(self, p_def)

        self.__logger = LogClient()

        self.__resource_case_def = OrcResource("CaseDef")
        self.__resource_step_def = OrcResource("StepDef")
        self.__resource_step_det = OrcResource("StepDet")
        self.__resource_item = OrcResource("Item")

    def service_add(self, p_data):
        """
        增加
        :param p_data:
        :return:
        """
        step_type = p_data["type"]
        step_id = p_data["step_id"]
        step_data = p_data["data"]

        if "ITEM" == step_type:

            # 增加 item
            result_item = self.__resource_item.post(parameter=step_data)

            # 检查结果
            if not ResourceCheck.result_status(result_item, u"新增步骤项", self.__logger):
                return False

            # 增加 step det
            result_step_det = self.__resource_step_det.post(
                parameter=dict(step_id=step_id, item_id=result_item.data["id"]))

            # 检查结果
            if not ResourceCheck.result_status(result_step_det, u"新增步骤", self.__logger):
                return False

            # 打印成功信息
            ResourceCheck.result_success(u"新增步骤", self.__logger)

        elif "FUNC" == step_type:

            # 增加 step det
            result_step_det = self.__resource_step_det.post(
                parameter=dict(step_id=step_id, item_id=step_data))

            # 检查结果
            if not ResourceCheck.result_status(result_step_det, u"新增步骤", self.__logger):
                return False

            # 打印成功信息
            ResourceCheck.result_success(u"新增步骤", self.__logger)

        return dict(step_id=step_id)

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        print 'dddd', p_list
        result = self.__resource_step_det.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除步骤", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除步骤", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        # 获取 item id
        result_step_det = self.__resource_step_det.get(path=p_data["id"])

        # 检查结果
        if not ResourceCheck.result_status(result_step_det, u"获取执行项ID", self.__logger):
            return False

        # 更新数据
        data = p_data.copy()
        data["id"] = result_step_det.data["item_id"]
        result_item = self.__resource_item.put(path=result_step_det.data["item_id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result_item, u"删除步骤", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除步骤", self.__logger)

        return result_item.status

    def service_search(self, p_cond):
        """
        删除
        :param p_cond:
        :return:
        """
        # 获取步骤类型
        if "step_id" not in p_cond:
            return list()

        step_info = self.__resource_step_def.get(path=p_cond["step_id"])

        # 检查结果
        if not ResourceCheck.result_status(step_info, u"获取步骤信息", self.__logger):
            return list()

        step_type = step_info.data["step_type"]

        # 查询 step det 列表
        result_step_det = self.__resource_step_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result_step_det, u"查询步骤", self.__logger):
            return list()

        # 查询 item id 列表
        item_id_list = [step_det["item_id"] for step_det in result_step_det.data]

        if "FUNC" == step_type:
            # 查询 func
            result_list = self.__resource_case_def.get(parameter=dict(id=item_id_list))

            # 检查结果
            if not ResourceCheck.result_status(result_list, u"查询步骤项", self.__logger):
                return list()

        else:
            # 查询 item 列表
            result_list = self.__resource_item.get(parameter=dict(id=item_id_list))

            # 检查结果
            if not ResourceCheck.result_status(result_list, u"查询步骤项", self.__logger):
                return list()

            for _item in result_list.data:
                if "item_operate" in _item:
                    _item["item_operate_text"] = operate_to_str(json.loads(_item["item_operate"]))

        # 打印成功信息
        ResourceCheck.result_success(u" 查询步骤", self.__logger)

        # 连接数据
        return connect_list(result_step_det.data, result_list.data, "item_id")

    def service_up(self, p_id):
        """
        上移
        :param p_id:
        :return:
        """
        result = self.__resource_step_det.post(path=p_id, parameter=dict(cmd="up"))

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
        result = self.__resource_step_det.post(path=p_id, parameter=dict(cmd="down"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"下移步骤", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"下移步骤", self.__logger)

        return result.status

    def service_get_step_type(self, p_step_id):
        """
        获取步骤类型
        :param p_step_id:
        :return:
        """
        result = self.__resource_step_def.get(path=p_step_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u" 获取步骤", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u" 查询步骤", self.__logger)

        return result.data["step_type"]


class ItemNormalModel(ItemModel):

    def __init__(self):

        ItemModel.__init__(self, 'Item')

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        return super(ItemNormalModel, self).service_add(p_data)

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        print p_list
        return super(ItemNormalModel, self).service_delete(p_list)

    def service_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        return super(ItemNormalModel, self).service_update(p_data)

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return super(ItemNormalModel, self).service_search(p_cond)


class ItemFuncModel(ItemModel):

    def __init__(self):

        ItemModel.__init__(self, 'Case')

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        return super(ItemFuncModel, self).service_add(p_data)

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        return super(ItemFuncModel, self).service_delete(p_list)

    def service_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        return super(ItemFuncModel, self).service_update(p_data)

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return super(ItemFuncModel, self).service_search(p_cond)