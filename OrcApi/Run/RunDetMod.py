import os

from OrcLib import get_config
from RunData import RunData


class RunDetMod(object):

    def __init__(self):

        object.__init__(self)

        self.__configer = get_config()

        self.__data = RunData()
        self.__home = self.__configer.get_option("RUN", "home")

    def usr_search(self, p_path):
        """
        :param p_path:
        :type p_path: dict
        :return:
        """
        if not isinstance(p_path, dict) or "path" not in p_path:
            return list()

        res_file = os.path.join(self.__home, p_path["path"], 'default.res')

        if not os.path.exists(res_file):
            return

        self.__data.load_list(res_file)

        return self.__data.list
