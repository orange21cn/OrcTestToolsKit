# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import asc

from OrcLib.LibCommon import gen_date_str
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import WebWidgetDet
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db


class WidgetDetHandle():
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):
        pass

    def usr_search(self, p_filter=None):
        """
        :param p_filter:
        :return:
        """
        if not p_filter:
            p_filter = dict()

        # search
        def f_value(p_flag):
            return "%%%s%%" % p_filter[p_flag]

        _res = self.__session.query(WebWidgetDet)

        if 'id' in p_filter:
            _res = _res.filter(WebWidgetDet.id.ilike(f_value('id')))

        if 'widget_id' in p_filter:
            _res = _res.filter(WebWidgetDet.widget_id == p_filter['widget_id'])

        if 'widget_env' in p_filter:
            _res = _res.filter(WebWidgetDet.widget_env.ilike(f_value('widget_env')))

        # add order
        _res = _res.order_by(asc(WebWidgetDet.widget_order))

        return _res.all()

    def usr_add(self, p_data):
        """

        :param p_data:
        :return:
        """
        _node = WebWidgetDet()

        # Create id
        _node.id = gen_id("widget_det")

        # widget_id
        _node.widget_id = p_data['widget_id'] if 'widget_id' in p_data else ""

        # widget_order
        _node.widget_order = p_data['widget_order'] if 'widget_order' in p_data else ""

        # widget_attr_type
        _node.widget_attr_type = p_data['widget_attr_type'] if 'widget_attr_type' in p_data else ""

        # widget_attr_value
        _node.widget_attr_value = p_data['widget_attr_value'] if 'widget_attr_value' in p_data else ""

        # widget_desc
        _node.widget_desc = p_data['widget_desc'] if 'widget_desc' in p_data else ""

        # comment
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
        t_item = self.__session.query(WebWidgetDet).filter(WebWidgetDet.batch_no == _no).first()

        if t_item is not None:
            return self._create_no()
        else:
            return _no

    def usr_modify(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(WebWidgetDet).filter(WebWidgetDet.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_list):

        if "list" in p_list:

            for t_id in p_list["list"]:
                 try:
                    # Delete current item
                    self.__session.query(WebWidgetDet).filter(WebWidgetDet.id == t_id).delete()
                 except Exception:
                    # Todo
                    self.__session.rollback()

        self.__session.commit()

