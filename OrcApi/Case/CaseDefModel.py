# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from sqlalchemy import func

from OrcLib.LibDatabase import TabCaseDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcApi.Batch.BatchDetModel import BatchDetHandle
from OrcApi.Case.CaseDetModel import CaseDetHandle


class CaseDefHandle:
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        self.__batch = BatchDetHandle()
        self.__case_det = CaseDetHandle()

    def usr_search(self, p_filter=None):
        """
        :param p_filter:
        :return:
        """
        _res_list = []

        # search
        def f_value(p_flag):
            return "%%%s%%" % p_filter[p_flag]

        if p_filter is None:
            i_res = self.__session.query(TabCaseDef).all()
        else:
            i_res = self.__session.query(TabCaseDef)

            if 'id' in p_filter:
                i_res = i_res.filter(TabCaseDef.id.ilike(f_value('id')))

            if 'pid' in p_filter:
                i_res = i_res.filter(TabCaseDef.pid.ilike(f_value('pid')))

            if 'case_no' in p_filter:
                i_res = i_res.filter(TabCaseDef.case_no.ilike(f_value('case_no')))

            if 'case_type' in p_filter:
                i_res = i_res.filter(TabCaseDef.case_type.ilike(f_value('case_type')))

            if 'case_name' in p_filter:
                i_res = i_res.filter(TabCaseDef.case_name.ilike(f_value('case_name')))

            if 'case_desc' in p_filter:
                i_res = i_res.filter(TabCaseDef.case_desc.ilike(f_value('case_desc')))

        # get tree
        for t_item in i_res:

            if t_item not in _res_list:
                t_tree = self._get_tree(self._get_root(t_item))
                _res_list.extend(t_tree)

        return _res_list

    def _get_root(self, p_item):
        """
        :param p_item:
        :return:
        """
        if p_item.pid is None:
            return p_item

        _res = self.__session.query(TabCaseDef).filter(TabCaseDef.id == p_item.pid).first()

        if _res.pid is None:
            return _res
        else:
            return self._get_root(_res)

    def _get_tree(self, p_item):
        """
        :param p_item:
        :return:
        """
        _tree = [p_item]
        _items = self.__session.query(TabCaseDef).filter(TabCaseDef.pid == p_item.id).all()

        for t_item in _items:
            _tree.extend(self._get_tree(t_item))

        return _tree

    def usr_add(self, p_data):
        """
        Add a new case
        :param p_data:
        :return:
        """
        _node = TabCaseDef()

        # Create id

        _node.id = gen_id("case_def")

        # pid
        _node.pid = p_data['pid'] if 'pid' in p_data else None

        # case_no
        _node.case_no = self._create_no(_node.pid)

        # case_name
        _node.case_name = p_data['case_name'] if 'case_name' in p_data else ""
        print "cc"
        # case_desc, comment
        _node.case_desc = p_data['case_desc'] if 'case_desc' in p_data else ""
        _node.case_type = p_data['case_type'] if 'case_type' in p_data else ""
        _node.comment = p_data['comment'] if 'comment' in p_data else ""

        # create_time, modify_time
        _node.create_time = datetime.now()
        _node.modify_time = datetime.now()
        print _node.to_json()
        print "KO"
        try:
            self.__session.add(_node)
            self.__session.commit()
        except:
            raise OrcDatabaseException

        self.usr_modify({"id": _node.id, "case_path": self.usr_get_path(_node.id)})

        return {u'id': str(_node.id)}

    def _create_no(self, p_id):
        """
        Create a no, like case_no
        :return:
        """
        _case_no = self.__session \
            .query(func.max(TabCaseDef.case_no)) \
            .filter(p_id == TabCaseDef.pid).first()[0]

        if _case_no is None:
            _case_no = 9

        return str(int(_case_no) + 1)

    def usr_modify(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabCaseDef).filter(TabCaseDef.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_list):

        if "list" in p_list:

            for t_id in p_list["list"]:
                self._del_tree(t_id)

        self.__session.commit()

    def _del_tree(self, p_id):

        def _del(_id):
            """
            Delete widget detail
            :param _id:
            :return:
            """
            # Delete it from batch
            _batch_list = self.__batch.usr_search({"case_id": _id})
            _batch_ids = dict(list=list(value.id for value in _batch_list))

            self.__batch.usr_delete(_batch_ids)

            # Delete case detail
            _case_det_list = self.__case_det.usr_search({"case_id": _id})
            _case_det_ids = dict(list=list(value.id for value in _case_det_list))

            self.__case_det.usr_delete(_case_det_ids)

        try:
            # Delete children
            _list = self.__session.query(TabCaseDef.id).filter(TabCaseDef.pid == p_id).all()

            for t_id in _list:
                _del(t_id[0])
                self._del_tree(t_id[0])

            # Delete current item
            _del(p_id)
            self.__session.query(TabCaseDef).filter(TabCaseDef.id == p_id).delete()

        except Exception:
            # Todo
            self.__session.rollback()

    def usr_list_search(self, p_filter):
        """
        :param p_filter:
        :return:
        """

        # search
        def f_value(p_flag):
            return "%%%s%%" % p_filter[p_flag]

        _res = self.__session.query(TabCaseDef)

        if 'id' in p_filter:
            _res = _res.filter(TabCaseDef.id.in_(p_filter['id']))

        if 'case_no' in p_filter:
            _res = _res.filter(TabCaseDef.case_no.ilike(f_value('case_no')))

        if 'case_name' in p_filter:
            _res = _res.filter(TabCaseDef.case_name.ilike(f_value('case_name')))

        return _res

    def usr_get_path(self, p_id):

        _no = self.__session.query(TabCaseDef.case_no).filter(TabCaseDef.id == p_id).first()
        _pid = self.__session.query(TabCaseDef.pid).filter(TabCaseDef.id == p_id).first()

        if _no is not None:
            _no = _no[0]
            _pid = _pid[0]

        if _pid is None:
            return _no
        else:
            _pid = _pid
            return "%s.%s" % (self.usr_get_path(_pid), _no)
