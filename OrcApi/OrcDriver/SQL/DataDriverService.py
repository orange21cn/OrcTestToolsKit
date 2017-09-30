# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLibFrame.LibData import OrcDataClient

class DataDriverService(object):

    def __init__(self):

        # resource
        self._resource_database = OrcResource('DataBase')

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self._resource_database.get(parameter=p_cond)
        if not ResourceCheck.result_status(result, 'Run sql failed %s' % p_cond):
            return False
        else:
            return result.data
