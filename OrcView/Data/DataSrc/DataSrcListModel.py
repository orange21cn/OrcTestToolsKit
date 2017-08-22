# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcView.Lib.LibTable import ModelTable


class DataSrcListModel(ModelTable):
    """

    """
    def __init__(self):

        ModelTable.__init__(self, 'DataSrc')

        self._logger = OrcLog('view.data.data_src.data_src_list_model')

        self._resource = OrcResource('DataSrc')

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        if not isinstance(p_data, dict):
            return []

        result = self._resource.post(parameter=p_data)

        if not ResourceCheck.result_status(result, u"新增数据源 % 失败", self._logger):
            return []

        return result.data

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        self._resource.delete(parameter=p_list)

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :type p_data: dict
        :return:
        """
        db_data = p_data

        current_data = self.mod_get_current_data()
        if not current_data:
            return

        current_id = current_data['id']
        db_data["id"] = current_id

        self._resource.put(path=current_id, parameter=p_data)

    def service_search(self, p_condition):
        """
        查询
        :param p_condition:
        :return:
        """
        result = self._resource.get()

        if not ResourceCheck.result_status(result, '查找数据源'):
            return list()

        return result.data
