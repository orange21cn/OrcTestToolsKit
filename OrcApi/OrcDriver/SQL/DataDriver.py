# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibCmd import DataCmd

from .DataDriverService import DataDriverService


class DataDriver(object):

    def __init__(self):

        object.__init__(self)

        # Log
        self._logger = OrcLog("driver.sql")

        # service
        self._service = DataDriverService()

        # 环境
        self._env = 'TEST'

    def execute(self, p_cmd):
        """
        执行
        :param p_cmd:
        :type p_cmd: DataCmd
        :return:
        """
        cmd_dict = p_cmd.get_cmd_dict()
        cmd_dict['ENV'] = self._env
        return self._service.service_search(cmd_dict)

    def set_env(self, p_env):
        """
        设置环境
        :param p_env:
        :return:
        """
        self._env = p_env
