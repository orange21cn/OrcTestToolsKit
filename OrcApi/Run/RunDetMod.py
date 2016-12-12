import os
from RunCore import RunCore


class RunDetMod:

    def __init__(self):

        self.__core = RunCore()
        self.__home = self.__core.get_home()

    def usr_search(self, p_path):
        """
        :param p_path:
        :type p_path: dict
        :return:
        """
        res_file = "%s/%s/default.res" % (self.__home, p_path["path"])

        if not os.path.exists(res_file):
            return

        self.__core.load_list(res_file)

        return self.__core.list
