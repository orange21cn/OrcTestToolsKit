# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import gen_date_str
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException

from OrcLib.LibDatabase import WebPageDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcApi.Driver.Web.PageDetModel import PageDetModel


class PageDefModel:
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        self.child = PageDetModel()

    def usr_search(self, p_filter=None):
        """
        :param p_filter:
        :return:
        """
        # search
        def f_value(p_flag):
            return "%%%s%%" % p_filter[p_flag]

        if p_filter is None:
            _res = self.__session.query(WebPageDef).all()
        else:
            _res = self.__session.query(WebPageDef)

            if 'id' in p_filter:
                _res = _res.filter(WebPageDef.id == p_filter['id'])

            if 'page_flag' in p_filter:
                _res = _res.filter(WebPageDef.page_flag.ilike(f_value('page_flag')))

            if 'page_desc' in p_filter:
                _res = _res.filter(WebPageDef.page_desc.ilike(f_value('page_desc')))

        return _res.all()

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

        return {u'id': str(_node.id)}

    def _create_no(self):
        """
        Create a no, like batch_no
        :return:
        """
        _no = gen_date_str()
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

    def usr_delete(self, p_list):

        if "list" in p_list:

            for t_id in p_list["list"]:

                _page_det_list = self.child.usr_search({"page_id": t_id})
                _page_det_ids = dict(list=list(value.id for value in _page_det_list))

                self.child.usr_delete(_page_det_ids)

                try:
                    # Delete current item
                    self.__session\
                        .query(WebPageDef)\
                        .filter(WebPageDef.id == t_id)\
                        .delete()
                except Exception:
                    # Todo
                    self.__session.rollback()

        self.__session.commit()
