# coding=utf-8
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibNet import OrcHttpService
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

        self.__service_web_driver = OrcHttpService("Driver")

    def launch_web_step(self, p_step_info):
        """
        WEB 类型用例执行项
        :param p_step_info:
        :return:
        """
        return self.__resource_web_driver.post(p_step_info)

    def check_web_step(self, p_step_info):
        """
        WEB 类型步骤检查项
        :param p_step_info:
        :return:
        """
        if "DATA" in p_step_info:
            step_data = p_step_info["DATA"]
            return self.__resource_web_driver.post(p_step_info) == step_data
        else:
            return self.__resource_web_driver.post(p_step_info)

    def get_web_pic(self, p_name):
        """
        获取截图
        :param p_name:
        :return:
        """
        self.__service_web_driver.save_pic(p_name)

    def get_item(self, p_item_id):
        """
        :param p_item_id:
        :return:
        :rtype: TabItem
        """
        self.__resource_item.set_path(p_item_id)
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
        :param p_data:
        :return:
        """
        import json
        self.__resource_view.get(json.dumps(p_data))
