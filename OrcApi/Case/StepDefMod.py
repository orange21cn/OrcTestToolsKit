# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import gen_date_str
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

    def usr_search(self, p_filter=None):
        """
        :param p_filter:
        :return:
        """
        # search
        def f_value(p_flag):
            return "%%%s%%" % p_filter[p_flag]

        if p_filter is None:
            _res = self.__session.query(TabStepDef).all()
        else:
            _res = self.__session.query(TabStepDef)

            if 'id' in p_filter:
                if isinstance(p_filter["id"], list):
                    _res = _res.filter(TabStepDef.id.in_(p_filter['id']))
                else:
                    _res = _res.filter(TabStepDef.id == p_filter['id'])

            if 'pid' in p_filter:
                _res = _res.filter(TabStepDef.pid == p_filter['pid'])

            if 'step_no' in p_filter:
                _res = _res.filter(TabStepDef.step_no.ilike(f_value('step_no')))

            if 'step_desc' in p_filter:
                _res = _res.filter(TabStepDef.step_desc.ilike(f_value('step_desc')))

        return _res.all()

    def usr_add(self, p_data):
        """
        Add a new step
        :param p_data:
        :return:
        """
        _node = TabStepDef()

        # Create id
        _node.id = gen_id("step_def")

        # step_no
        _node.step_no = self._create_no()

        # step_desc, comment
        _node.step_desc = p_data['step_desc'] if 'step_desc' in p_data else ""
        _node.step_type = p_data['step_type'] if 'step_type' in p_data else ""
        _node.comment = p_data['comment'] if 'comment' in p_data else ""

        # create_time, modify_time
        _node.create_time = datetime.now()
        _node.modify_time = datetime.now()

        try:
            self.__session.add(_node)
            self.__session.commit()
        except:
            raise OrcDatabaseException

        return _node

    def _create_no(self):
        """
        Create a no, like step_no
        :return:
        """
        _no = gen_date_str()
        t_item = self.__session.query(TabStepDef).filter(TabStepDef.step_no == _no).first()

        if t_item is not None:
            return self._create_no()
        else:
            return _no

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

        # search
        def f_value(p_flag):
            return "%%%s%%" % p_filter[p_flag]

        _res = self.__session.query(TabStepDef)

        if 'id' in p_filter:
            _res = _res.filter(TabStepDef.id.in_(p_filter['id']))

        if 'step_no' in p_filter:
            _res = _res.filter(TabStepDef.step_no.ilike(f_value('step_no')))

        if 'step_desc' in p_filter:
            _res = _res.filter(TabStepDef.step_desc.ilike(f_value('step_name')))

        return _res.all()
