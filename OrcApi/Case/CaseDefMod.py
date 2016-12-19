# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import func

from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabCaseDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcApi.Batch.BatchDetMod import BatchDetMod
from OrcApi.Case.CaseDetMod import CaseDetMod


class CaseDefMod:
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        self.__batch = BatchDetMod()
        self.__case_det = CaseDetMod()

    def usr_search(self, p_cond=None):
        """
        根据条件查询,但不包括子用例和你用例
        :param p_cond: 条件
        :type p_cond: dict
        :return:
        """
        # 判断输入参数是否为空
        cond = p_cond if p_cond else dict()

        # 查询条件 like
        _like = lambda p_flag: "%%%s%%" % cond[p_flag]

        # db session
        result = self.__session.query(TabCaseDef)

        if 'id' in p_cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(TabCaseDef.id.in_(cond['id']))
            else:
                result = result.filter(TabCaseDef.id == cond['id'])

        if 'pid' in p_cond:
            result = result.filter(TabCaseDef.pid == cond['pid'])

        if 'case_no' in p_cond:
            result = result.filter(TabCaseDef.case_no == cond['case_no'])

        if 'case_type' in p_cond:
            result = result.filter(TabCaseDef.case_type == cond['case_type'])

        if 'case_name' in p_cond:
            result = result.filter(TabCaseDef.case_name.ilike(_like('case_name')))

        if 'case_desc' in p_cond:
            result = result.filter(TabCaseDef.case_desc.ilike(_like('case_desc')))

        return result.all()

    def usr_search_all(self, p_cond):
        """
        查询包含用例的树,追踪到根节点
        :param p_cond:
        :type p_cond: dict
        :return:
        :rtype: list
        """
        result = list()

        for _case in self.usr_search(p_cond):

            if _case not in result:

                # 获取当前用例的根用例组
                _root = self.__get_root(_case)

                # 获取根用例组的所有子用例
                _tree = self.__get_tree(_root)

                # 加入结果树
                result.extend(_tree)

        return result

    def usr_search_tree(self, p_id):
        """
        查询用例组及其所有子用例
        :param p_id:
        :return:
        :rtype: list
        """
        case = self.usr_search(dict(id=p_id))

        if case:
            return self.__get_tree(case[0])
        else:
            return list()

    def usr_search_path(self, p_id):
        """
        获取CASE的路径
        :param p_id: case id
        :return: 10.11.14 ....
        :rtype: str
        """
        case_data = self.__session.query(TabCaseDef).filter(TabCaseDef.id == p_id).first()

        case_no = case_data.case_no if case_data else None
        case_pid = case_data.pid if case_data else None

        if case_pid:
            return "%s.%s" % (self.usr_get_path(case_pid), case_no)
        else:
            return case_no

    def __get_root(self, p_item):
        """
        :param p_item:
        :type p_item: TabCaseDef
        :return:
        """
        if not p_item or not p_item.pid:
            return p_item

        res = self.__session.query(TabCaseDef).filter(TabCaseDef.id == p_item.pid).first()

        if res and res.pid is not None:
            return self.__get_root(res)
        else:
            return res

    def __get_tree(self, p_item):
        """
        :param p_item:
        :type p_item: TabCaseDef
        :return:
        """
        _tree = [p_item]
        _items = self.__session.query(TabCaseDef).filter(TabCaseDef.pid == p_item.id).all()

        for t_item in _items:
            _tree.extend(self.__get_tree(t_item))

        return _tree

    def usr_add(self, p_data):
        """
        Add a new case
        :param p_data:
        :return:
        """
        _node = TabCaseDef()

        # Create id

        _node.id = gen_id("case_def")

        # pid
        _node.pid = p_data['pid'] if 'pid' in p_data else None

        # case_no
        _node.case_no = self._create_no(_node.pid)

        # case_name
        _node.case_name = p_data['case_name'] if 'case_name' in p_data else ""

        # case_desc, comment
        _node.case_desc = p_data['case_desc'] if 'case_desc' in p_data else ""
        _node.case_type = p_data['case_type'] if 'case_type' in p_data else ""
        _node.comment = p_data['comment'] if 'comment' in p_data else ""

        # create_time, modify_time
        _node.create_time = datetime.now()
        _node.modify_time = datetime.now()

        try:
            self.__session.add(_node)
            self.__session.commit()
        except:
            raise OrcDatabaseException

        self.usr_update({"id": _node.id, "case_path": self.usr_get_path(_node.id)})

        return _node

    def _create_no(self, p_id):
        """
        Create a no, like case_no
        :return:
        """
        _case_no = self.__session \
            .query(func.max(TabCaseDef.case_no)) \
            .filter(p_id == TabCaseDef.pid).first()[0]

        if _case_no is None:
            _case_no = 9

        return str(int(_case_no) + 1)

    def usr_update(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(TabCaseDef).filter(TabCaseDef.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):
        self.__session.query(TabCaseDef).filter(TabCaseDef.id == p_id).delete()
        self.__session.commit()

    def usr_list_search(self, p_filter):
        """
        :param p_filter:
        :return:
        """

        # search
        def f_value(p_flag):
            return "%%%s%%" % p_filter[p_flag]

        _res = self.__session.query(TabCaseDef)

        if 'id' in p_filter:
            _res = _res.filter(TabCaseDef.id.in_(p_filter['id']))

        if 'case_no' in p_filter:
            _res = _res.filter(TabCaseDef.case_no.ilike(f_value('case_no')))

        if 'case_name' in p_filter:
            _res = _res.filter(TabCaseDef.case_name.ilike(f_value('case_name')))

        return _res

    def usr_get_path(self, p_id):
        """
        查询路径,新接口中用 search_path 代替
        :param p_id:
        :return:
        """
        _no = self.__session.query(TabCaseDef.case_no).filter(TabCaseDef.id == p_id).first()
        _pid = self.__session.query(TabCaseDef.pid).filter(TabCaseDef.id == p_id).first()

        if _no is not None:
            _no = _no[0]
            _pid = _pid[0]

        if _pid is None:
            return _no
        else:
            return "%s.%s" % (self.usr_get_path(_pid), _no)
