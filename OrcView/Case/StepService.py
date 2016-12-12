# coding=utf-8
from OrcLib.LibNet import OrcHttpNewResource
from OrcLib.LibApi import connect_list


class StepService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_step_det = OrcHttpNewResource("StepDet")
        self.__resource_item = OrcHttpNewResource("Item")

    def usr_add(self, p_data):
        """
        增加
        :param p_data:
        :return:
        """
        # 增加 item
        item = self.__resource_item.post(p_data)

        # 增加 step det
        step_id = p_data["step_id"]
        item_id = item["id"]
        step_data = dict(step_id=step_id, item_id=item_id)
        self.__resource_step_det.post(step_data)

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

        # 连接数据
        return connect_list(step_det_list, item_list, "item_id")
