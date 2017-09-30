# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import OrcSocketResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibCmd import OrcCmd
from OrcLib.LibDatabase import TabItem
from OrcLib.LibProgram import OrcDataStruct
from OrcLibFrame.LibData import OrcDataClient

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
        self.__data_client = OrcDataClient()

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

    def get_data(self, p_env, p_def_list, p_object_id):
        """
        获取数据,获取则返回,未获取报错
        :param p_env:
        :param p_object_id:
        :param p_def_list:
        :type p_def_list: list
        :return:
        """
        for _node in OrcDataStruct.iterator_reversed_list(p_def_list):

            _cmd = OrcRecordCmd(_node)
            _scope = _cmd.get_scope()

            self.__data_client.set_env(p_env)

            result = self.__data_client.get_one(_scope, _cmd.id, p_object_id)

            if result:
                return result
        else:
            return None
