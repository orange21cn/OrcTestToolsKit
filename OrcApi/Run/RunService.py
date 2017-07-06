# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibDatabase import TabItem
from OrcLib.LibProgram import OrcDataStruct

from RunData import RunCmdType


class RunCoreService(object):
    """
    运行核心模块,负责目录管理,list 管理和执行三部分
    """
    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog("resource.run.run_core.service")

        self.__resource_web_driver = OrcResource("Driver")
        self.__resource_item = OrcResource("Item")
        self.__resource_data = OrcResource("Data")

    def launch_web_step(self, p_step_info):
        """
        WEB 类型用例执行项
        :param p_step_info:
        :return:
        """
        result = self.__resource_web_driver.post(parameter=p_step_info)

        # 检查结果
        if not ResourceCheck.result_status(result, u"执行WEB执行项", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"执行WEB执行项", self.__logger)

        return result.status

    def check_web_step(self, p_step_info):
        """
        WEB 类型步骤检查项
        :param p_step_info:
        :return:
        """
        if "DATA" in p_step_info:
            step_data = p_step_info["DATA"]
            result = self.__resource_web_driver.post(parameter=p_step_info)

            # 检查结果
            if not ResourceCheck.result_status(result, u"获取WEB执行结果数据", self.__logger):
                return False

            # 打印成功信息
            ResourceCheck.result_success(u"获取WEB执行结果数据", self.__logger)

            result_data = result.data

            return step_data == result_data

        else:
            result = self.__resource_web_driver.post(parameter=p_step_info)

            # 检查结果
            if not ResourceCheck.result_status(result, u"获取WEB执行结果", self.__logger):
                return False

            # 打印成功信息
            ResourceCheck.result_success(u"获取WEB执行结果", self.__logger)

            return result.status

    def get_web_pic(self, p_name):
        """
        获取截图
        :param p_name:
        :return:
        """
        self.__resource_web_driver.save_pic(p_name)

    def get_item(self, p_item_id):
        """
        获取对象
        :param p_item_id:
        :return:
        :rtype: TabItem
        """
        result = self.__resource_item.get(path=p_item_id)

        # 检查结果
        if not ResourceCheck.result_status(result, u"获取对象", self.__logger):
            return None

        # 打印成功信息
        ResourceCheck.result_success(u"获取对象", self.__logger)

        return TabItem(result.data)

    def get_data(self, p_def_list, p_object_id):
        """
        获取数据
        :param p_object_id:
        :param p_def_list:
        :type p_def_list: list
        :return:
        """
        for _node in OrcDataStruct.iterator_reversed_list(p_def_list):

            _cmd = RunCmdType(_node)

            if _cmd.is_batch_type():
                _type = 'BATCH'
            elif _cmd.is_case_type():
                _type = 'CASE'
            elif _cmd.is_step_type():
                _type = 'STEP'
            elif _cmd.is_item_type():
                _type = 'ITEM'
            else:
                _type = ''

            result = self.__resource_data.get(
                parameter=dict(src_id=_cmd.id, src_type=_type, data_flag=p_object_id))

            # 检查结果
            if not ResourceCheck.result_status(result, u"获取%s数据" % _type, self.__logger):
                continue

            # 打印成功信息
            ResourceCheck.result_success(u"获取%s数据" % _type, self.__logger)

            if result.data:
                break
        else:
            return None

        if result.data:
            return result.data[0]["data_value"]
        else:
            return None
