# coding=utf-8
import json
import socket

from OrcLib import get_config
from OrcLib.LibLog import OrcLog


class OrcDriver(object):

    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog("driver.web.selenium")
        self.__driver_configer = get_config("driver")

        # IP
        self.__ip = self.__driver_configer.get_option('DRIVER', 'ip')

        # port
        self.__port = int(self.__driver_configer.get_option('DRIVER', 'port'))

        # 截图
        self.__pic_name = self.__driver_configer.get_option("WEB", "pic_name")

    def start(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.__ip, self.__port))
        sock.listen(1)

        while True:

            connection, address = sock.accept()

            try:
                connection.settimeout(5)

                _cmd = json.loads(connection.recv(1024))

                self.__logger.info("Run command %s" % _cmd)

                if ("quit" in _cmd) and ("QUIT" == _cmd["quit"]):
                    if self.__root is not None:
                        self.__root.quit()
                    break

                _result = self.__execute(_cmd)

                connection.send(str(_result))

            except socket.timeout:
                self.__logger.error("time out")
                connection.send(str(False))

            except Exception:
                self.__logger.error("Driver run command failed!")
                connection.send(str(False))

            connection.close()
