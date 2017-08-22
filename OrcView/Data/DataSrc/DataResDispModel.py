# coding=utf-8
from OrcLib import get_config
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck

from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibViewDef import ViewDefinition
from OrcView.Lib.LibMain import LogClient


class DataResDispModel(ModelTable):
    """

    """
    def __init__(self):

        ModelTable.__init__(self)

        self._logger = LogClient()

        self._configer = get_config('data_src')
        self._resource = OrcResource('DataBase')
        self._db_id = None

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :type p_cond: dict
        :return:
        """
        if self._db_id is None:
            return list()

        condition = p_cond.copy()
        condition['DATA_SRC'] = self._db_id
        condition['TYPE'] = 'DEBUG'

        result = self._resource.get(parameter=condition)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询结果", self._logger):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"查询结果", self._logger)

        # 表头
        fields = result.data['FIELDS']

        self._definition = ViewDefinition([dict(
            ID=item, NAME=item, TYPE="LINETEXT", DISPLAY=True) for item in fields])

        # 表数据
        data = result.data['DATA']

        result = list()
        for _item in data:
            nvs = zip(fields, _item)
            result.append(dict((name, value) for name, value in nvs))

        return result

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        pass

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        pass

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        pass

    def service_set_db(self, p_id):
        """
        设置数据库
        :param p_id:
        :return:
        """
        self._db_id = p_id
