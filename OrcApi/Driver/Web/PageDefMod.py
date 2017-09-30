# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import OrcString
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException

from OrcLib.LibDatabase import WebPageDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcApi.Driver.Web.PageDetMod import PageDetMod


class PageDefMod:
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        self.child = PageDetMod()

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
        result = self.__session.query(WebPageDef)

        if 'id' in cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(WebPageDef.id.in_(cond['id']))
            else:
                result = result.filter(WebPageDef.id == cond['id'])

        if 'page_flag' in cond:
            result = result.filter(WebPageDef.page_flag.ilike(_like('page_flag')))

        if 'page_desc' in cond:
            result = result.filter(WebPageDef.page_desc.ilike(_like('page_desc')))

        return result.all()

    def usr_add(self, p_data):
        """
        :param p_data:
        :return:
        """
        _node = WebPageDef()

        # Create id
        _node.id = gen_id("page_def")

        # page_flag
        _node.page_flag = p_data['page_flag'] if 'page_flag' in p_data else ""

        # page_desc
        _node.page_desc = p_data['page_desc'] if 'page_desc' in p_data else ""

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
        _no = OrcString.get_data_str()
        t_item = self.__session.query(WebPageDef).filter(WebPageDef.batch_no == _no).first()

        if t_item is not None:
            return self._create_no()
        else:
            return _no

    def usr_update(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(WebPageDef).filter(WebPageDef.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):

        self.__session.query(WebPageDef).filter(WebPageDef.id == p_id).delete()
        self.__session.commit()
