# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException

from OrcLib.LibDatabase import TabBatchDet
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db


class BatchDetModel(TabBatchDet):
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        TabBatchDet.__init__(self)

    def usr_search(self, p_filter=None):
        """
        :param p_filter:
        :return:
        """
        _res = self.__session.query(TabBatchDet)

        if 'id' in p_filter:
            _res = _res.filter(TabBatchDet.id == p_filter('id'))

        if 'batch_id' in p_filter:
            _res = _res.filter(TabBatchDet.batch_id == p_filter['batch_id'])

        if 'case_id' in p_filter:
            _res = _res.filter(TabBatchDet.case_id == p_filter['case_id'])

        return _res.all()

    def usr_add(self, p_data):
        """
        :param p_data:
        :return:
        """
        _batch_id = p_data["batch_id"]
        _case_ids = p_data["case"]

        for _case_id in _case_ids:

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

        return {u'id': str(_batch_id)}

    def usr_modify(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabBatchDet).filter(TabBatchDet.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_list):

        if "list" in p_list:

            for t_id in p_list["list"]:
                self.__session.query(TabBatchDet).filter(TabBatchDet.id == t_id).delete()

        self.__session.commit()
