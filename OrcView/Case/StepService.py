# coding=utf-8
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibApi import connect_list


class ItemService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_case_def = OrcHttpResource("CaseDef")
        self.__resource_step_det = OrcHttpResource("StepDet")
        self.__resource_item = OrcHttpResource("Item")

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
            item = self.__resource_item.post(step_data)

            # 增加 step det
            step_id = step_id
            item_id = item["id"]
            step_det_data = dict(step_id=step_id, item_id=item_id)

            self.__resource_step_det.post(step_det_data)

        elif "FUNC" == step_type:

            # 增加 step det
            step_id = step_id
            func_id = step_data
            step_det_data = dict(step_id=step_id, item_id=func_id)

            self.__resource_step_det.post(step_det_data)

        return dict(step_id=step_id)

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        return self.__resource_step_det.delete(p_list)

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        # 获取 item id
        self.__resource_step_det.set_path(p_data["id"])
        item_id = self.__resource_step_det.get()["item_id"]

        # 更新数据
        data = p_data.copy()
        data["id"] = item_id
        self.__resource_item.set_path(item_id)

        return self.__resource_item.put(p_data)

    def usr_search(self, p_cond):
        """
        删除
        :param p_cond:
        :return:
        """
        # 查询 step det 列表
        step_det_list = self.__resource_step_det.get(p_cond)

        # 查询 item id 列表
        item_id_list = [step_det["item_id"] for step_det in step_det_list]

        # 查询 item 列表
        item_list = self.__resource_item.get(dict(id=item_id_list))

        # 查询 func
        case_list = self.__resource_case_def.get(dict(id=item_id_list))

        # func 转成 item 结构
        func_list = [dict(
            id=case["id"],
            item_no=case["case_no"],
            item_mode="",
            item_type="",
            item_operate=case["case_path"],
            item_desc=case["case_desc"],
            comment=case["comment"],
            create_time=case["create_time"],
            modify_time=case["modify_time"]
        )for case in case_list]

        # 连接 list
        item_list.extend(func_list)

        # 连接数据
        return connect_list(step_det_list, item_list, "item_id")


class StepService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_step_def = OrcHttpResource("StepDef")

    def view_get_step_type(self, p_step_id):

        self.__resource_step_def.set_path(p_step_id)
        return self.__resource_step_def.get()["step_type"]
