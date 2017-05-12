# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import asc

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import WebWidgetDet
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db


class WidgetDetMod:
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):
        pass

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
        result = self.__session.query(WebWidgetDet)

        if 'id' in cond:
            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(WebWidgetDet.id.in_(cond['id']))
            else:
                result = result.filter(WebWidgetDet.id == cond['id'])

        if 'widget_id' in cond:
            result = result.filter(WebWidgetDet.widget_id == cond['widget_id'])

        if 'widget_order' in cond:
            result = result.filter(WebWidgetDet.widget_order == cond['widget_order'])

        if 'widget_env' in cond:
            result = result.filter(WebWidgetDet.widget_env.ilike(_like('widget_env')))

        # add order
        result = result.order_by(asc(WebWidgetDet.widget_order))

        return result.all()

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
        _node.widget_order = self._create_no(_node.widget_id)

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

        return _node

    def _create_no(self, p_widget_id):
        """
        Create a no, like batch_no
        :return:
        """
        max_order = self.__session \
            .query(func.max(WebWidgetDet.widget_order)) \
            .filter(p_widget_id == WebWidgetDet.widget_id).first()[0]

        if max_order is None:
            max_order = 9

        return str(int(max_order) + 1)

    def usr_update(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(WebWidgetDet).filter(WebWidgetDet.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):

        self.__session.query(WebWidgetDet).filter(WebWidgetDet.id == p_id).delete()
        self.__session.commit()
