# coding=utf-8
from OrcLib.LibNet import OrcResource


class SqlDriverService(object):

    def __init__(self):

        # resource
        self._resource_database = OrcResource('DataBase')

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return self._resource_database.get(parameter=p_cond)