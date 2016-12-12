# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import gen_date_str
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import WebPageDet
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db


class PageDetMod():
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
        result = self.__session.query(WebPageDet)

        if 'id' in cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(WebPageDet.id.in_(cond['id']))
            else:
                result = result.filter(WebPageDet.id == cond['id'])

        if 'page_id' in cond:
            result = result.filter(WebPageDet.page_id == cond['page_id'])

        if 'page_env' in cond:
            result = result.filter(WebPageDet.page_env.ilike(_like('page_env')))

        return result.all()

    def usr_add(self, p_data):
        """

        :param p_data:
        :return:
        """
        _node = WebPageDet()

        # Create id
        _node.id = gen_id("page_det")

        # page_id
        _node.page_id = p_data['page_id'] if 'page_id' in p_data else ""

        # page_env
        _node.page_env = p_data['page_env'] if 'page_env' in p_data else ""

        # page_url
        _node.page_url = p_data['page_url'] if 'page_url' in p_data else ""

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

    def _create_no(self):
        """
        Create a no, like batch_no
        :return:
        """
        _no = gen_date_str()
        t_item = self.__session.query(WebPageDet).filter(WebPageDet.batch_no == _no).first()

        if t_item is not None:
            return self._create_no()
        else:
            return _no

    def usr_update(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(WebPageDet).filter(WebPageDet.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):

        self.__session.query(WebPageDet).filter(WebPageDet.id == p_id).delete()
        self.__session.commit()
