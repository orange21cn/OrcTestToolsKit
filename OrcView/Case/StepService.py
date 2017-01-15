# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibApi import connect_list
from OrcView.Lib.LibView import ResourceCheck


class ItemService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_case_def = OrcResource("CaseDef")
        self.__resource_step_det = OrcResource("StepDet")
        self.__resource_item = OrcResource("Item")

    def usr_add(self, p_data):
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
            if not ResourceCheck.result_status(result_item, u"新增步骤项"):
                return False

            # 增加 step det
            result_step_det = self.__resource_step_det.post(
                parameter=dict(step_id=step_id, item_id=result_item.data["id"]))

            # 检查结果
            if not ResourceCheck.result_status(result_step_det, u"新增步骤"):
                return False

            # 打印成功信息
            ResourceCheck.result_success(u"新增步骤")

        elif "FUNC" == step_type:

            # 增加 step det
            result_step_det = self.__resource_step_det.post(
                parameter=dict(step_id=step_id, item_id=step_data))

            # 检查结果
            if not ResourceCheck.result_status(result_step_det, u"新增步骤"):
                return False

            # 打印成功信息
            ResourceCheck.result_success(u"新增步骤")

        return dict(step_id=step_id)

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_step_det.delete(p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除步骤")

        return result.status

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        # 获取 item id
        result_step_det = self.__resource_step_det.get(path=p_data["id"])

        # 检查结果
        if not ResourceCheck.result_status(result_step_det, u"获取执行项ID"):
            return False

        # 更新数据
        data = p_data.copy()
        data["id"] = result_step_det.data["item_id"]
        result_item = self.__resource_item.put(path=result_step_det.data["item_id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result_item, u"删除步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除步骤")

        return result_item.status

    def usr_search(self, p_cond):
        """
        删除
        :param p_cond:
        :return:
        """
        # 查询 step det 列表
        result_step_det = self.__resource_step_det.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result_step_det, u"查询步骤"):
            return list()

        # 查询 item id 列表
        item_id_list = [step_det["item_id"] for step_det in result_step_det.data]

        # 查询 item 列表
        result_item = self.__resource_item.get(parameter=dict(id=item_id_list))

        # 检查结果
        if not ResourceCheck.result_status(result_item, u"查询步骤项"):
            return list()

        # 查询 func
        # case_list = self.__resource_case_def.get(dict(id=item_id_list))
        #
        # # func 转成 item 结构
        # func_list = [dict(
        #     id=case["id"],
        #     item_no=case["case_no"],
        #     item_mode="",
        #     item_type="",
        #     item_operate=case["case_path"],
        #     item_desc=case["case_desc"],
        #     comment=case["comment"],
        #     create_time=case["create_time"],
        #     modify_time=case["modify_time"]
        # )for case in case_list]
        #
        # # 连接 list
        # item_list.extend(func_list)

        # 打印成功信息
        ResourceCheck.result_success(u" 查询步骤")

        # 连接数据
        return connect_list(result_step_det.data, result_item.data, "item_id")

    def usr_up(self, p_id):
        """
        上移
        :return:
        """
        result = self.__resource_step_det.post(path=p_id, parameter=dict(cmd="up"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"上移步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"上移步骤")

        return result.status

    def usr_down(self, p_id):
        """
        下移
        :return:
        """
        result = self.__resource_step_det.post(path=p_id, parameter=dict(cmd="down"))

        # 检查结果
        if not ResourceCheck.result_status(result, u"下移步骤"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"下移步骤")

        return result.status


class StepService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_step_def = OrcResource("StepDef")

    def view_get_step_type(self, p_step_id):
        """
        获取步骤类型
        :param p_step_id:
        :return:
        """
        result = self.__resource_step_def.get(path=p_step_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u" 获取步骤"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u" 查询步骤")

        return result.data["step_type"]
