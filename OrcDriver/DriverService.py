from OrcLib.LibNet import OrcSocketResource


class WebDriverService:

    def __init__(self):

        self.__resource_socket = OrcSocketResource("SERVER_WEB_001")

    def run(self, p_cmd):
        return self.__resource_socket.get(p_cmd)
