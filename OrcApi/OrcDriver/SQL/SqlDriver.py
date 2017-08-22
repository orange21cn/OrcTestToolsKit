# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibCmd import DataCmd

from .SqlDriverService import SqlDriverService


class SqlDriver(object):

    def __init__(self):

        object.__init__(self)

        # Log
        self._logger = OrcLog("driver.sql")

        # service
        self._service = SqlDriverService()

    def execute(self, p_cmd):
        """
        执行
        :param p_cmd:
        :return:
        """
        sql_command = DataCmd(p_cmd)

        return self._service.service_search(sql_command.get_cmd_dict())
