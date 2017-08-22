# coding=utf-8
import json

from OrcLib.LibProgram import OrcFactory
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibDatabase import TabData


class OrcDataClient(object):

    def __init__(self):

        object.__init__(self)

        # Log
        self._logger = OrcLog('basic.lib_data')

        # Data resource
        self._resource_data = OrcResource('Data')

        # DataBase resource
        self._resource_database = OrcResource('DataBase')

    def get_data(self, p_env, p_src_type, p_src_id, p_data_flag):
        """
        获取数据
        :param p_data_flag:
        :param p_src_id:
        :param p_src_type:
        :param p_env:
        :return:
        """
        result = self._resource_data.get(parameter=dict(
            test_env=p_env,
            src_id=p_src_id,
            src_type=p_src_type,
            data_flag=p_data_flag))

        if not ResourceCheck.result_status(result, u"读取数据", self._logger):
            return None

        if not result.data:
            return None

        res_data = TabData(result.data[0])

        if 'STR' == res_data.data_mode:
            return res_data.data_value
        elif 'INT' == res_data.data_mode:
            return int(res_data.data_value)
        elif 'SQL' == res_data.data_mode:
            try:
                return self._search_sql(p_env, json.loads(res_data.data_value))
            except ValueError:
                return None
        else:
            return None

    def _search_sql(self, p_env, p_data):
        """
        根据
        :param p_env:
        :param p_data: {SOURCE, SQL}
        :return:
        """
        data = OrcFactory.create_default_dict(p_data)
        data_src = "%s.%s" % (data.value('SRC'), p_env)
        sql = data.value('VALUE')

        result = self._resource_database.get(parameter=dict(DATA_SRC=data_src, SQL=sql, TYPE='DATA'))

        if not ResourceCheck.result_status(result, "获取 SQL 数据 %s:%s" % (data_src, sql)):
            return None

        return result.data
