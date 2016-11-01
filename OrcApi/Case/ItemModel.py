# -*- coding: utf-8 -*-
import json
from datetime import datetime

from OrcLib.LibCommon import gen_date_str
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabItem
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db


class ItemModel:
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
        _res = self.__session.query(TabItem)

        if 'id' in p_filter:
            _res = _res.filter(TabItem.id == p_filter['id'])

        return _res.all()

    def usr_list_search(self, p_filter):
        """
        :param p_filter:
        :return:
        """
        # search
        _res = self.__session.query(TabItem)

        if 'id' in p_filter:
            _res = _res.filter(TabItem.id.in_(p_filter['id']))

        return _res.all()

    def usr_add(self, p_data):
        """
        Add a new case
        :param p_data:
        :return:
        """
        _node = TabItem()

        # Create id
        _node.id = gen_id("item")

        # case_no
        _node.item_no = self._create_no()

        # item_type
        _node.item_type = p_data['item_type'] if 'item_type' in p_data else ""

        # item_mode
        _node.item_mode = p_data['item_mode'] if 'item_mode' in p_data else ""

        # item_operate
        _node.item_operate = json.dumps(p_data['item_operate']) if 'item_operate' in p_data else ""

        # item_desc
        _node.item_desc = p_data['item_desc'] if 'item_desc' in p_data else ""

        # case_desc, comment
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
        Create a no, like case_no
        :return:
        """
        _no = gen_date_str()
        t_item = self.__session.query(TabItem).filter(TabItem.item_no == _no).first()

        if t_item is not None:
            return self._create_no()
        else:
            return _no

    def usr_update(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabItem).filter(TabItem.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_list):

        if "list" in p_list:

            for t_id in p_list["list"]:

                try:
                    # Delete current item
                    self.__session.query(TabItem).filter(TabItem.id == t_id).delete()

                except Exception:
                    # Todo
                    self.__session.rollback()

        self.__session.commit()



