# coding=utf-8
import gc
import json
import socket

from OrcLib import get_config
from OrcLib.LibCmd import OrcCmd
from OrcLib.LibCmd import OrcDriverCmd
from OrcLib.LibCmd import DataCmd
from OrcLib.LibCmd import WebCmd
from OrcLib.LibCmd import OrcSysCmd
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResult
from OrcLib.LibStatus import OrcDriverStatus
from Web.WebDriver import WebDriver
from SQL.DataDriver import DataDriver


class OrcDriver(object):

    class Driver:

        web = WebDriver()

        data = DataDriver()

        def __init__(self):
            pass

    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog("driver.web.selenium")
        self.__configer_driver = get_config('driver')

        # IP
        self.__ip = self.__configer_driver.get_option('DEFAULT', 'ip')

        # port
        self.__port = int(self.__configer_driver.get_option('DEFAULT', 'port'))

        # 驱动名称
        self.__name = self.__configer_driver.get_option('DEFAULT', 'name')

        # 截图
        self.__pic_name = self.__configer_driver.get_option("WEB", "pic_name")

        # WEB 驱动
        self._driver = self.Driver()

        # 状态
        self._status = OrcDriverStatus(self.__name)

        self._status.set_waiting()
        self._status.set_idle()

        # session
        self._session = None

        # 循环标识
        self._loop_flag = True

    def start(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.__ip, self.__port))
        sock.listen(1)

        self.__logger.info("Start driver server on %s:%s" % (self.__ip, self.__port))

        while self._loop_flag:

            connection, address = sock.accept()

            result = OrcResult()

            try:
                result.reset()

                # 接收数据
                connection.settimeout(5)
                res_data = json.loads(connection.recv(1024))

                # 驱动忙
                self._status.set_busy()

                self.__logger.info("Run command %s" % res_data)

                command = OrcCmd(res_data)

                # 执行系统命令
                if command.is_system():

                    sys_command = command.cmd

                    _res = self.launch_system_command(sys_command, command.session)

                    result.set_status(True)
                    result.set_data(_res)
                    result.set_message('Run system command succeed.')

                # 发送命令给驱动
                elif command.is_driver():

                    # 检查 session
                    if self._session != command.session:
                        return False

                    driver_command = command.cmd
                    assert isinstance(driver_command, OrcDriverCmd)

                    # 执行 web 命令
                    if driver_command.is_web():

                        web_command = driver_command.cmd
                        _res = self._driver.web.execute(web_command)

                        result.set_status(True)
                        result.set_data(_res)
                        result.set_message('Run web command succeed')

                    # 执行 sql 命令
                    elif driver_command.is_data():
                        # Todo
                        sql_command = driver_command.cmd
                        assert isinstance(sql_command, DataCmd)

                        _res = self._driver.data.execute(sql_command)

                        result.set_status(True)
                        result.set_data(_res)
                        result.set_message('Run sql command succeed')

                # 其他情况
                else:
                    result.set_message("Unknown command type: %s" % command.type)

                self.__logger.info("Result is %s" % result.rtn())

                # 释放驱动状态
                self._status.set_idle()

                connection.send(json.dumps(result.rtn()))

            except socket.timeout:
                self.__logger.error("Time out")

                result.set_status(False)
                result.set_message('Time out.')

                connection.send(json.dumps(result.rtn()))

            except Exception:
                self.__logger.error("Driver run command failed!")

                result.set_status(False)
                result.set_message('Unknown error.')

                connection.send(json.dumps(result.rtn()))

            connection.close()

        # 释放内存
        del self._driver
        gc.collect()

    def launch_system_command(self, p_command, p_session):
        """
        运行系统命令
        :param p_session:
        :param p_command:
        :return:
        """
        assert isinstance(p_command, OrcSysCmd)

        # 退出
        if p_command.is_quit():
            self._loop_flag = False

            web_cmd = WebCmd()
            web_cmd.set_driver()
            web_cmd.set_cmd_operation('QUIT')

            self._driver.web.execute(web_cmd)

        # 占用服务
        elif p_command.is_occupy():

            if self._session is not None:
                return False
            else:
                self._session = p_session
                self._status.set_occupy(p_session)
                return True

        # 释放服务
        elif p_command.is_release():
            self._session = None
            self._status.set_waiting()
            return True

        # 设置参数(驱动所需其他参数)
        elif p_command.is_parameter():
            _parameter = p_command.get_data()
            self.__configer_driver.set_option('DEFAULT', 'environment', _parameter['env'])
            self.__configer_driver.set_option('WEB', 'browser', _parameter['browser'])

        # 其他
        else:
            pass
