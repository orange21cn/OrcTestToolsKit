# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibProgram import OrcFactory


class DataSrcDispModel(object):
    """
    数据源详细信息操作模型
    """
    def __init__(self):

        object.__init__(self)

        # Log
        self._logger = OrcLog('view.data.data_src.data_src_list_model')

        # Resource
        self._resource = OrcResource('DataSrc')

        self._src_info = None

        self._src_id = None

        self._env = None

    def mod_add(self, p_data):
        """
        新增, 暂未使用
        :param p_data: 新增数据 {ID, TYPE...}
        :return:
        """
        if not isinstance(p_data, dict):
            return False

        result = self._resource.post(parameter=p_data)

        if not ResourceCheck.result_status(result, u"新增数据源出错 %s, %s" % p_data, self._logger):
            return False

        return True

    def mod_delete(self, p_id):
        """
        删除, 暂未使用
        :param p_id: 数据源 id
        :return:
        """
        result = self._resource.delete(path=p_id)

        if not ResourceCheck.result_status(result, u"删除数据源出错 %s, %s" % p_id, self._logger):
            return False

        return True

    def mod_update(self, p_id, p_data):
        """
        修改
        :param p_id:
        :return:
        """
        if not isinstance(p_data, dict):
            return False

        result = self._resource.put(path=p_id, parameter=p_data)

        if not ResourceCheck.result_status(result, u"更新数据源出错 %s, %s" % (p_id, p_data), self._logger):
            return False

        return True

    def mod_search(self, p_cond=None, p_env=None):
        """
        查询
        :param p_env:
        :param p_cond: 查询条件
        :return:
        """
        if isinstance(p_cond, dict):
            self._src_info = p_cond

        if self._src_info is None:
            return dict()

        src_info = OrcFactory.create_default_dict(self._src_info)

        self._src_id = src_info.value('id')
        self._env = p_env if p_env is not None else self._env

        db_id = src_info.value('id')
        if p_env:
            db_id = "%s.%s" % (db_id, p_env)

        result = self._resource.get(parameter=dict(id=db_id))

        if not ResourceCheck.result_status(result, u"查询数据源信息 %s" % p_cond, self._logger):
            return dict()

        db_info = OrcFactory.create_default_dict(None if not result.data else result.data[0])
        db_info.add('name', src_info.value('name'))
        db_info.add('desc', src_info.value('desc'))

        return db_info.dict()

    def mod_get_db_id(self):
        """
        获取 db id,用于数据库查询,所以不发送 src_id,env 为空时返回 空
        :return:
        """
        return None if not self._env else "%s.%s" % (self._src_id, self._env)
