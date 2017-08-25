# -*- coding: utf-8 -*-
import json
from datetime import datetime

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabItem
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db


class ItemMod:
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

        # db session
        result = self.__session.query(TabItem)

        if 'id' in cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(TabItem.id.in_(cond['id']))
            else:
                result = result.filter(TabItem.id == cond['id'])

        return result.all()

    def usr_add(self, p_data):
        """
        Add a new case
        :param p_data:
        :return:
        """
        _node = TabItem()

        # Create id
        _node.id = gen_id("item")

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

        return _node

    def usr_update(self, p_cond):
        """
        更新
        :param p_cond:
        :return:
        """
        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabItem).filter(TabItem.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):
        """

        :param p_id:
        :return:
        """
        self.__session.query(TabItem).filter(TabItem.id == p_id).delete()
        self.__session.commit()
