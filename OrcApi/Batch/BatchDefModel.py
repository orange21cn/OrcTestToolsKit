# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import gen_date_str
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabBatchDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db


class BatchDefHandle(TabBatchDef):
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        TabBatchDef.__init__(self)

    def usr_get_value(self, p_id):

        # search
        _res = self.__session.query(TabBatchDef)\
            .filter(TabBatchDef.id == p_id)

        return _res.first()

    def usr_search(self, p_filter=None):
        """
        :param p_filter:
        :return:
        """
        _returns = []

        # search
        def f_value(p_flag):
            return "%%%s%%" % p_filter[p_flag]

        if p_filter is None:

            i_res = self.__session.query(TabBatchDef).all()
        else:
            i_res = self.__session.query(TabBatchDef)

            if 'id' in p_filter:
                print f_value('id')
                i_res = i_res.filter(TabBatchDef.id == p_filter['id'])

            if 'pid' in p_filter:
                i_res = i_res.filter(TabBatchDef.pid.ilike(f_value('pid')))

            if 'batch_no' in p_filter:
                i_res = i_res.filter(TabBatchDef.batch_no.ilike(f_value('batch_no')))

            if 'batch_name' in p_filter:
                i_res = i_res.filter(TabBatchDef.batch_name.ilike(f_value('batch_name')))

            if 'batch_desc' in p_filter:
                i_res = i_res.filter(TabBatchDef.batch_desc.ilike(f_value('batch_desc')))

        # get tree
        for t_item in i_res:
            if t_item not in _returns:
                t_tree = self._get_tree(self._get_root(t_item))
                _returns.extend(t_tree)

        return _returns

    def _get_root(self, p_item):
        """
        :param p_item:
        :return:
        """
        if p_item.pid is None:
            return p_item

        _res = self.__session.query(TabBatchDef).filter(TabBatchDef.id == p_item.pid).first()

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
        _items = self.__session.query(TabBatchDef).filter(TabBatchDef.pid == p_item.id).all()

        for t_item in _items:
            _tree.extend(self._get_tree(t_item))

        return _tree

    def usr_add(self, p_data):
        """

        :param p_data:
        :return:
        """
        _node = TabBatchDef()

        # Create id
        _node.id = gen_id("batch_def")

        # batch_no
        _node.batch_no = self._create_no()

        # pid
        _node.pid = p_data['pid'] if 'pid' in p_data else None

        # batch_name
        _node.batch_name = p_data['batch_name'] if 'batch_name' in p_data else ""

        # batch_desc, comment
        _node.batch_desc = p_data['batch_desc'] if 'batch_desc' in p_data else ""
        _node.comment = p_data['comment'] if 'comment' in p_data else ""

        # create_time, modify_time
        _node.create_time = datetime.now()
        _node.modify_time = datetime.now()

        try:
            self.__session.add(_node)
            self.__session.commit()
        except:
            raise OrcDatabaseException

        return {u'id': str(_node.id)}

    def _create_no(self):
        """
        Create a no, like batch_no
        :return:
        """
        _no = gen_date_str()
        t_item = self.__session.query(TabBatchDef).filter(TabBatchDef.batch_no == _no).first()

        if t_item is not None:
            return self._create_no()
        else:
            return _no

    def usr_modify(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabBatchDef).filter(TabBatchDef.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_list):

        if "list" in p_list:

            for t_id in p_list["list"]:
                self._del_tree(t_id)

        self.__session.commit()

    def _del_tree(self, p_id):

        try:
            # Delete child
            _list = self.__session.query(TabBatchDef).filter(TabBatchDef.pid == p_id)
            for t_item in _list:
                self._del_tree(t_item.id)

            # Delete current item
            self.__session.query(TabBatchDef).filter(TabBatchDef.id == p_id).delete()
        except Exception:
            # Todo
            self.__session.rollback()

    def usr_get_path(self, p_id):

        _no = self.__session.query(TabBatchDef.batch_no).filter(TabBatchDef.id == p_id).first()[0]
        _pid = self.__session.query(TabBatchDef.pid).filter(TabBatchDef.id == p_id).first()[0]

        if _pid is None:
            return _no
        else:
            return "%s.%s" % (self.usr_get_path(_pid), _no)
