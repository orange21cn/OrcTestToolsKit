# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException

from OrcLib.LibDatabase import TabBatchDet
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcLib.LibLog import OrcLog


class BatchDetMod(TabBatchDet):
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        TabBatchDet.__init__(self)

        self.__logger = OrcLog("api.batch.mod.batch_det")

    def usr_search(self, p_cond=None):
        """
        :param p_cond:
        :return:
        """
        # 判断输入参数是否为空
        cond = p_cond if p_cond else dict()

        # db session
        result = self.__session.query(TabBatchDet)

        if 'id' in p_cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(TabBatchDet.id.in_(cond['id']))
            else:
                result = result.filter(TabBatchDet.id == cond['id'])

        if 'batch_id' in p_cond:
            result = result.filter(TabBatchDet.batch_id == p_cond['batch_id'])

        if 'case_id' in p_cond:
            result = result.filter(TabBatchDet.case_id == p_cond['case_id'])

        return result.all()

    def usr_add(self, p_data):
        """
        :param p_data:
        :return:
        """
        _batch_id = p_data["batch_id"]
        _case_id = p_data["case_id"]

        _node = TabBatchDet()

        # Create id
        _node.id = gen_id("batch_det")

        # batch_id
        _node.batch_id = _batch_id

        # case_id
        _node.case_id = _case_id

        # create_time, modify_time
        _node.create_time = datetime.now()

        try:
            self.__session.add(_node)
        except:
            raise OrcDatabaseException

        self.__session.commit()

        return _node

    def usr_modify(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabBatchDet).filter(TabBatchDet.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):

        self.__session.query(TabBatchDet).filter(TabBatchDet.id == p_id).delete()
        self.__session.commit()
