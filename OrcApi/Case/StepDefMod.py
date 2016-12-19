# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabStepDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcApi.Case.StepDetMod import StepDetMod


class StepDefMod:
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        self.__step_det = StepDetMod()

    def usr_search(self, p_cond=None):
        """
        :param p_cond:
        :return:
        """
        # 判断输入参数是否为空
        cond = p_cond if p_cond else dict()

        # 查询条件 like
        _like = lambda p_flag: "%%%s%%" % cond[p_flag]

        # db session
        result = self.__session.query(TabStepDef)

        if 'id' in p_cond:

            # 查询支持多 id
            if isinstance(p_cond["id"], list):
                result = result.filter(TabStepDef.id.in_(p_cond['id']))
            else:
                result = result.filter(TabStepDef.id == p_cond['id'])

        if 'pid' in p_cond:
            result = result.filter(TabStepDef.pid == p_cond['pid'])

        if 'step_desc' in p_cond:
            result = result.filter(TabStepDef.step_desc.ilike(_like('step_desc')))

        return result.all()

    def usr_add(self, p_data):
        """
        Add a new step
        :param p_data:
        :return:
        """
        _node = TabStepDef()

        # Create id
        _node.id = gen_id("step_def")

        # step_desc
        _node.step_desc = p_data['step_desc'] if 'step_desc' in p_data else ""

        # step_type
        _node.step_type = p_data['step_type'] if 'step_type' in p_data else ""

        # comment
        _node.comment = p_data['comment'] if 'comment' in p_data else ""

        # create_time, modify_time
        _node.create_time = datetime.now()

        # modify_time
        _node.modify_time = datetime.now()

        try:
            self.__session.add(_node)
            self.__session.commit()
        except:
            raise OrcDatabaseException

        return _node

    def usr_update(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabStepDef).filter(TabStepDef.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):

        self.__session.query(TabStepDef).filter(TabStepDef.id == p_id).delete()
        self.__session.commit()

    def usr_list_search(self, p_filter):
        """
        To be deleted
        :param p_filter:
        :return:
        """
        # Todo 条件太少
        # search
        def f_value(p_flag):
            return "%%%s%%" % p_filter[p_flag]

        _res = self.__session.query(TabStepDef)

        if 'id' in p_filter:
            _res = _res.filter(TabStepDef.id.in_(p_filter['id']))

        if 'step_desc' in p_filter:
            _res = _res.filter(TabStepDef.step_desc.ilike(f_value('step_name')))

        return _res.all()
