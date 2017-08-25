# coding=utf-8
import re

from OrcLib.LibCmd import DataCmd
from OrcLib.LibCmd import OrcCmd
from OrcLib.LibCmd import OrcSysCmd
from OrcLib.LibCommon import DateStr
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcSocketResource
from OrcLib.LibNet import ResourceCheck
from OrcLibFrame.LibRunTime import OrcRunTime


class DriverSession(OrcRunTime):
    """
    session 管理
    """
    def __init__(self):

        OrcRunTime.__init__(self, 'DRIVER')

        # 记录 key/session 的关系, {key:session}
        self.session = None

    def create_session(self):
        """
        生成 session
        :return:
        """
        # session 查找重复和占用不是同时,大迸发时可能存在问题,暂不考虑
        exist_sessions = [item[2] for item in self.get_module_values() if re.match('\.OCCUPY', item[0])]

        for i in range(100):
            _seq = "0%s" % i if 10 > i else str(i)
            session = "%s%s" % (DateStr.get_long_str(), _seq)

            if session in exist_sessions:
                continue
            else:
                self.session = session
                break
        else:
            return False

        return True

    @staticmethod
    def get_session():
        """
        获取 session
        :return:
        """
        driver_session = DriverSession()
        driver_session.create_session()
        return driver_session.session


class DriverClient(object):
    """
    驱动客户端,用于一次性驱动调试调用
    """
    def __init__(self):

        object.__init__(self)

        self._logger = OrcLog('basic.lib.driver.driver_client')

        self._command = OrcCmd()
        self._sys_command = OrcSysCmd()
        self._data_command = DataCmd()

        self._driver = OrcSocketResource('Driver')

    def execute_web(self):
        """

        :return:
        """
        pass

    def execute_sql(self, p_data_src, p_sql):
        """
        执行 sql
        :param p_sql:
        :param p_data_src:
        :return:
        """
        self._occupy()

        self._data_command.set_mode(p_data_src)
        self._data_command.set_object(p_sql)
        self._command.set_cmd(self._data_command)

        result = self._driver.get(self._command.get_cmd_dict())

        self._release()

        if not ResourceCheck.result_status(result, "Run sql command %s" % self._command.get_cmd_dict(), self._logger):
            return list()

        return result.data

    def _occupy(self):
        """
        占用驱动
        :return:
        """
        self._sys_command.set_occupy()
        self._command.set_session(DriverSession().get_session())
        self._command.set_cmd(self._sys_command)

        result = self._driver.get(self._command.get_cmd_dict())

        if not ResourceCheck.result_status(result, '占用驱动', self._logger):
            return False

        return True

    def _release(self):
        """
        释放驱动
        :return:
        """
        self._sys_command.set_release()
        self._command.set_cmd(self._sys_command)

        result = self._driver.get(self._command.get_cmd_dict())

        if not ResourceCheck.result_status(result, '释放驱动', self._logger):
            return False

        return True
