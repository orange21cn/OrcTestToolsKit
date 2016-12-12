# -*- coding: utf-8 -*-
from sqlalchemy import func

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabRunTime
from OrcLib.LibDatabase import orc_db
from OrcLib.LibLog import OrcLog


class RunTimeMod(TabRunTime):
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        TabRunTime.__init__(self)

        self.__logger = OrcLog("api.run_time.mod")

    def usr_search(self, p_cond=None):
        """
        :param p_cond:
        :return:
        """
        # 判断输入参数是否为空
        cond = p_cond if p_cond else dict()

        # db session
        result = self.__session.query(TabRunTime)

        if 'id' in cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(TabRunTime.id.in_(cond['id']))
            else:
                result = result.filter(TabRunTime.id == cond['id'])

        if 'module' in cond:
            result = result.filter(TabRunTime.module == cond['module'])

        if 'data_flag' in cond:
            result = result.filter(TabRunTime.data_flag == cond['data_flag'])

        if 'data_index' in cond:
            result = result.filter(TabRunTime.data_index == cond['data_index'])

        return result.all()

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        node = TabRunTime()

        # module
        node.module = p_data['module'] if 'module' in p_data else None

        # data_flag
        node.data_flag = p_data['data_flag'] if 'data_flag' in p_data else None

        # data_index
        node.data_index = self.__create_index(p_data)

        # data_value
        node.data_value = p_data['data_value'] if 'data_value' in p_data else None

        try:
            self.__session.add(node)
            self.__session.commit()
        except:
            raise OrcDatabaseException

        return node

    def usr_update(self, p_cond):

        for _id in p_cond:

            if "id" == _id:
                continue

            _data = None if is_null(p_cond[_id]) else p_cond[_id]
            _item = self.__session.query(TabRunTime).filter(TabRunTime.id == p_cond['id'])
            _item.update({_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        self.__session.query(TabRunTime).filter(TabRunTime.id == p_id).delete()
        self.__session.commit()

    def __create_index(self, p_data):
        """
        Create a no, like case_no
        :return:
        """
        if "module" not in p_data or "data_flag" not in p_data:
            return None

        _module = p_data["module"]
        _flag = p_data["data_flag"]
        _case_no = self.__session \
            .query(func.max(TabRunTime.data_index)) \
            .filter(_module == TabRunTime.module) \
            .filter(_flag == TabRunTime.data_flag) \
            .first()[0]

        if _case_no is None:
            _case_no = 0

        return str(int(_case_no) + 1)
