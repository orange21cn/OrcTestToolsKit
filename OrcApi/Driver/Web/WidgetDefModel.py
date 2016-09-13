# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import gen_date_str
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import WebWidgetDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db

from OrcApi.Driver.Web.WidgetDetModel import WidgetDetHandle


class WidgetDefHandle:
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        self.child = WidgetDetHandle()

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
            i_res = self.__session.query(WebWidgetDef).all()
        else:
            i_res = self.__session.query(WebWidgetDef)

            if 'id' in p_filter:
                i_res = i_res.filter(WebWidgetDef.id == p_filter['id'])

            if 'widget_id' in p_filter:
                i_res = i_res.filter(WebWidgetDef.widget_id == p_filter['widget_id'])

            if 'widget_type' in p_filter:
                i_res = i_res.filter(WebWidgetDef.widget_type == p_filter['widget_type'])

            if 'widget_flag' in p_filter:
                i_res = i_res.filter(WebWidgetDef.widget_flag.ilike(f_value('widget_flag')))

            if 'widget_desc' in p_filter:
                i_res = i_res.filter(WebWidgetDef.widget_desc.ilike(f_value('widget_desc')))

        _res = i_res.all()
        if 0 == len(_res):
            return []

        # get tree
        for t_item in i_res.all():

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

        _res = self.__session.query(WebWidgetDef).filter(WebWidgetDef.id == p_item.pid).first()

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
        _items = self.__session.query(WebWidgetDef).filter(WebWidgetDef.pid == p_item.id).all()

        for t_item in _items:
            _tree.extend(self._get_tree(t_item))

        return _tree

    def usr_add(self, p_data):
        """
        :param p_data:
        :return:
        """
        _node = WebWidgetDef()

        # Create id
        _node.id = gen_id("widget_def")

        # pid
        _node.pid = p_data['pid'] if 'pid' in p_data else None

        # widget_flag
        _node.widget_flag = p_data['widget_flag'] if 'widget_flag' in p_data else ""

        # widget_type
        _node.widget_type = p_data['widget_type'] if 'widget_type' in p_data else ""

        # widget_desc
        _node.widget_desc = p_data['widget_desc'] if 'widget_desc' in p_data else ""

        # batch_desc, comment
        _node.comment = p_data['comment'] if 'comment' in p_data else ""

        # create_time, modify_time
        _node.create_time = datetime.now()
        _node.modify_time = datetime.now()

        try:
            self.__session.add(_node)
            self.__session.commit()
        except:
            raise OrcDatabaseException

        # Modify
        self.usr_modify({"id": _node.id,
                         "widget_path": self.usr_get_path(_node.id)})

        return {u'id': str(_node.id)}

    def _create_no(self):
        """
        Create a no, like batch_no
        :return:
        """
        _no = gen_date_str()
        t_item = self.__session.query(WebWidgetDef).filter(WebWidgetDef.batch_no == _no).first()

        if t_item is not None:
            return self._create_no()
        else:
            return _no

    def usr_modify(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(WebWidgetDef).filter(WebWidgetDef.id == p_cond['id'])
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
            _widget_det_list = self.child.usr_search({"widget_id": _id})
            _widget_det_ids = dict(list=list(value.id for value in _widget_det_list))

            self.child.usr_delete(_widget_det_ids)

        try:
            # Delete children
            _list = self.__session.query(WebWidgetDef.id).filter(WebWidgetDef.pid == p_id).all()

            for t_id in _list:
                _del(t_id)  # Delete widget detail
                self._del_tree(t_id)  # Delete widget definition

            # Delete current item
            _del(p_id)  # Delete detail
            self.__session\
                .query(WebWidgetDef)\
                .filter(WebWidgetDef.id == p_id)\
                .delete()  # Delete widget definitio

        except Exception:
            # Todo
            self.__session.rollback()

    def usr_get_path(self, p_id):

        _no = self.__session.query(WebWidgetDef.widget_flag).filter(WebWidgetDef.id == p_id).first()
        _pid = self.__session.query(WebWidgetDef.pid).filter(WebWidgetDef.id == p_id).first()

        if _no is not None:
            _no = _no[0]
            _pid = _pid[0]

        if _pid is None:
            return _no
        else:
            return "%s.%s" % (self.usr_get_path(_pid), _no)
