# coding=utf-8
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibNet import OrcSocketResource
from OrcLib.LibDatabase import TabItem


class RunCoreService:
    """
    运行核心模块,负责目录管理,list 管理和执行三部分
    """
    def __init__(self):

        self.__resource_web_driver = OrcHttpResource("Driver")
        self.__resource_item = OrcHttpResource("Item")
        self.__resource_data = OrcHttpResource("Data")
        self.__resource_view = OrcSocketResource("View")

    def run_step(self, p_run_dict):

        return self.__resource_web_driver.post(p_run_dict)

    def get_item(self, p_item_id):
        """
        :param p_item_id:
        :return:
        :rtype: TabItem
        """
        self.__resource_item.set_id(p_item_id)
        item_data = self.__resource_item.get()

        if not item_data:
            return None
        else:
            return TabItem(item_data)

    def get_data(self, p_def_list, p_object_id):
        """tab_data
        :param p_object_id:
        :param p_def_list:
        :type p_def_list: list
        :return:
        """
        p_def_list.reverse()

        for _node in p_def_list:

            _id = _node["id"]
            _type = _node["run_det_type"]

            if _type in ("CASE", "CASE_GROUP"):
                _type = "CASE"
            elif _type in ("BATCH", "BATCH_GROUP"):
                _type = "BATCH"
            else:
                pass

            _data = self.__resource_data.get(
                dict(src_id=_id, src_type=_type, data_flag=p_object_id))

            if _data:
                break
        else:
            return None

        p_def_list.reverse()

        return _data[0]["data_value"]

    def update_status(self, p_data):
        """
        更新界面状态
        :return:
        """
        import json
        self.__resource_view.get(json.dumps(p_data))
