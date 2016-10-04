# -*- coding: utf-8 -*-
from datetime import datetime
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import WebWindowDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcLib.LibLog import OrcLog


class WindowDefModel:
    """
    Test data management
    """
    __session = orc_db.session
    __logger = OrcLog("api.driver.web.window_def")

    def __init__(self):
        pass

    def usr_search(self, p_filter=None):
        """
        查询符合条件的控件
        :param p_filter:
        :return:
        """
        # 判断输入参数是否为空
        _filter = p_filter if p_filter else dict()

        # 查询条件 like
        _like = lambda p_flag: "%%%s%%" % _filter[p_flag]

        # db session
        _search = self.__session.query(WebWindowDef)

        if 'id' in _filter:
            _search = _search.filter(WebWindowDef.id == _filter['id'])

        if 'window_mark' in _filter:
            _search = _search.filter(WebWindowDef.window_mark == _filter['window_mark'])

        if 'window_desc' in _filter:
            _search = _search.filter(WebWindowDef.window_desc.ilike(_like('window_desc')))

        if 'comment' in _filter:
            _search = _search.filter(WebWindowDef.comment.ilike(_like('comment')))

        return _search.all()

    def usr_add(self, p_data):
        """
        :param p_data:
        :return:
        """
        _node = WebWindowDef()

        # Create id
        _node.id = p_data['id']

        # window_mark
        _node.window_mark = p_data['window_mark'] if 'window_mark' in p_data else ""

        # window_desc
        _node.window_desc = p_data['window_desc'] if 'window_desc' in p_data else ""

        # batch_desc, comment
        _node.comment = p_data['comment'] if 'comment' in p_data else ""

        # create_time, modify_time
        _node.create_time = datetime.now()
        _node.modify_time = datetime.now()

        try:
            self.__session.add(_node)
            self.__session.commit()
        except:
            self.__logger.error("")
            raise OrcDatabaseException

        return dict(id=str(_node.id))

    def usr_modify(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(WebWindowDef).filter(WebWindowDef.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_list):

        if "list" in p_list:

            for t_id in p_list["list"]:
                self.__session.query(WebWindowDef).filter(WebWindowDef.id == t_id).delete()

        self.__session.commit()
