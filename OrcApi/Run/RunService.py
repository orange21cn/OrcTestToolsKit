# coding=utf-8
import os

from OrcLib import get_config
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import OrcSocketResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibCmd import OrcCmd
from OrcLib.LibDatabase import TabItem
from OrcLib.LibProgram import OrcDataStruct

from OrcLib.LibCmd import OrcRecordCmd


class RunCoreService(object):
    """
    运行核心模块,负责目录管理,list 管理和执行三部分
    """
    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog("resource.run.run_core.service")

        self.__resource_web_driver = OrcResource("Driver")

        self.__resource_driver = OrcSocketResource('Driver')
        self.__resource_item = OrcResource("Item")
        self.__resource_data = OrcResource("Data")

    def new_launch_web_step(self, p_cmd):
        """
        执行一个命令
        :param p_cmd:
        :type p_cmd: OrcCmd
        :return:
        """
        result = self.__resource_driver.get(p_cmd.get_cmd_dict())

        return result

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

            _cmd = OrcRecordCmd(_node)

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
