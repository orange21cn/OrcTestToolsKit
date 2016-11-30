# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabStepDet
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcApi.Case.ItemMod import ItemMod


class StepDetMod():
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        self.__item = ItemMod()

    def usr_search(self, p_filter=None):
        """
        :param p_filter:
        :return:
        """
        _res = self.__session.query(TabStepDet)

        if 'id' in p_filter:
            if isinstance(p_filter["id"], list):
                _res = _res.filter(TabStepDet.id.in_(p_filter['id']))
            else:
                _res = _res.filter(TabStepDet.id == p_filter['id'])

        if 'step_id' in p_filter:
            _res = _res.filter(TabStepDet.step_id == p_filter['step_id'])

        if 'item_id' in p_filter:
            _res = _res.filter(TabStepDet.item_id == p_filter['item_id'])

        return _res.all()

    def usr_add(self, p_data):
        """
        Add item
        :param p_data:
        :return:
        """
        _step_id = p_data["step_id"]
        _item_id = p_data["item_id"]

        _node = TabStepDet()

        # Create id
        _node.id = gen_id("step_det")

        # case_id
        _node.step_id = _step_id

        # step_id
        _node.item_id = _item_id

        # create_time, modify_time
        _node.create_time = datetime.now()

        try:
            self.__session.add(_node)
        except:
            raise OrcDatabaseException

        self.__session.commit()

        return _node

    def usr_update(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabStepDet).filter(TabStepDet.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):

        self.__session.query(TabStepDet).filter(TabStepDet.id == p_id).delete()
        self.__session.commit()

    def usr_list_search(self, p_list):

        _rtn = self.__session.query(TabStepDet).filter(TabStepDet.id.in_(p_list))
        return list(value.item_id for value in _rtn)
