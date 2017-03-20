# coding=utf-8
import json

from .LibLog import OrcLog
from .LibNet import OrcResource
from .LibNet import ResourceCheck
from .LibDatabase import TabData


class OrcDataClient(object):

    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog('basic.lib_data')
        self.__resource = OrcResource('Data')

    def get_data(self, p_env, p_src_type, p_src_id, p_data_flag, p_data_mode):
        """
        获取数据
        :param p_data_mode:
        :param p_data_flag:
        :param p_src_id:
        :param p_src_type:
        :param p_env:
        :return:
        """
        result = self.__resource.get(parameter=dict(
            test_env=p_env,
            src_id=p_src_id,
            src_type=p_src_type,
            data_flag=p_data_flag,
            data_mode=p_data_mode))

        if not ResourceCheck.result_status(result, u"读取数据", self.__logger):
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
                return self.search_sql(json.loads(res_data.data_value))
            except ValueError:
                return None
        else:
            return None

    def search_sql(self, p_data):
        """
        根据
        :param p_data: {SOURCE, SQL}
        :return:
        """
        # Todo
        pass
