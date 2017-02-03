# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import asc

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabStepDet
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcApi.Case.ItemMod import ItemMod


class StepDetMod(object):
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        object.__init__(self)

        self.__item = ItemMod()

    def usr_search(self, p_cond=None):
        """
        :param p_cond:
        :return:
        """
        print p_cond, "---------------------------"
        # 判断输入参数是否为空
        cond = p_cond if p_cond else dict()

        # db session
        result = self.__session.query(TabStepDet)

        if 'id' in cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(TabStepDet.id.in_(cond['id']))
            else:
                result = result.filter(TabStepDet.id == cond['id'])

        if 'step_id' in cond:
            result = result.filter(TabStepDet.step_id == cond['step_id'])

        if 'item_id' in cond:
            result = result.filter(TabStepDet.item_id == cond['item_id'])

        if 'item_no' in cond:
            result = result.filter(TabStepDet.item_no == cond['item_no'])

        result = result.order_by(asc(TabStepDet.item_no))

        return result.all()

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

        # step_no
        _node.item_no = self.__create_no(_step_id)

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

    def __create_no(self, p_step_id):
        """
        创建 case no
        :param p_step_id:
        :return:
        """
        case_no = self.__session\
            .query(func.max(TabStepDet.item_no))\
            .filter(p_step_id == TabStepDet.step_id)\
            .first()[0]

        if case_no is None:
            case_no = 9

        return str(int(case_no) + 1)