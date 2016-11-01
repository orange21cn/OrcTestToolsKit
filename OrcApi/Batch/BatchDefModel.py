# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import gen_date_str
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabBatchDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db


class BatchDefModel(TabBatchDef):
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

    def usr_search(self, p_cond=None):
        """
        :param p_cond:
        :return:
        """
        # 判断输入参数是否为空
        cond = p_cond if p_cond else dict()

        # 查询条件 like
        func_like = lambda p_flag: "%%%s%%" % cond[p_flag]

        search = self.__session.query(TabBatchDef)

        if 'id' in cond:
            search = search.filter(TabBatchDef.id == cond['id'])

        if 'pid' in cond:
            search = search.filter(TabBatchDef.pid == cond('pid'))

        if 'batch_no' in cond:
            search = search.filter(TabBatchDef.batch_no == cond('batch_no'))

        if 'batch_name' in cond:
            search = search.filter(TabBatchDef.batch_name.ilike(func_like('batch_name')))

        if 'batch_desc' in cond:
            search = search.filter(TabBatchDef.batch_desc.ilike(func_like('batch_desc')))

        return search.all()

    def usr_search_all(self, p_cond):
        """
        查询 batch 所有节点直至根节点
        :param p_cond:
        :return:
        """
        result = list()

        for _batch in self.usr_search(p_cond):

            if _batch not in result:

                # 获取当前用例的根用例组
                _root = self.__get_root(_batch)

                # 获取根用例组的所有子用例
                _tree = self.__get_tree(_root)

                # 加入结果树
                result.extend(_tree)

        return result

    def usr_search_tree(self, p_id):
        """
        获取节点及其所有子节点
        :return:
        """
        batch = self.usr_search(dict(id=p_id))

        if batch:
            return self.__get_tree(batch[0])
        else:
            return list()

    def usr_search_path(self, p_id):
        """
        获取路径至根节点
        :return:
        """
        batch_data = self.__session.query(TabCaseDef).filter(TabCaseDef.id == p_id).first()

        batch_no = batch_data.case_no if batch_data else None
        batch_pid = batch_data.pid if batch_data else None

        if batch_pid:
            return "%s.%s" % (self.usr_get_path(batch_pid), batch_no)
        else:
            return batch_no

    def __get_root(self, p_item):
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

    def __get_tree(self, p_item):
        """
        :param p_item:
        :return:
        """
        _tree = [p_item]
        _items = self.__session.query(TabBatchDef).filter(TabBatchDef.pid == p_item.id).all()

        for _item in _items:
            _tree.extend(self.__get_tree(_item))

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
        _node.batch_no = self.__create_no()

        # batch_type
        _node.batch_type = p_data['batch_type'] if 'batch_type' in p_data else None

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

    def __create_no(self):
        """
        Create a no, like batch_no
        :return:
        """
        _no = gen_date_str()
        t_item = self.__session.query(TabBatchDef).filter(TabBatchDef.batch_no == _no).first()

        if t_item is not None:
            return self.__create_no()
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
