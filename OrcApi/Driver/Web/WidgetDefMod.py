# -*- coding: utf-8 -*-
from datetime import datetime
from OrcLib.LibCommon import gen_date_str
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import WebWidgetDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcApi.Driver.Web.WidgetDetMod import WidgetDetMod


class WidgetDefMod:
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        self.child = WidgetDetMod()

    def usr_search(self, p_cond=None):
        """
        查询符合条件的控件
        :param p_cond:
        :return:
        """
        # 判断输入参数是否为空
        cond = p_cond if p_cond else dict()

        # 查询条件 like
        _like = lambda p_flag: "%%%s%%" % cond[p_flag]

        # db session
        result = self.__session.query(WebWidgetDef)

        if 'id' in cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(WebWidgetDef.id.in_(cond['id']))
            else:
                result = result.filter(WebWidgetDef.id == cond['id'])

        if 'widget_id' in cond:
            result = result.filter(WebWidgetDef.widget_id == cond['widget_id'])

        if 'widget_type' in cond:
            result = result.filter(WebWidgetDef.widget_type == cond['widget_type'])

        if 'widget_flag' in cond:
            result = result.filter(WebWidgetDef.widget_flag.ilike(_like('widget_flag')))

        if 'widget_desc' in cond:
            result = result.filter(WebWidgetDef.widget_desc.ilike(_like('widget_desc')))

        return result.all()

    def usr_search_all(self, p_filter):
        """
        查询符合条件的控件,追述到根节点,获取整棵树
        :param p_filter:
        :return:
        """
        _res_tree = []
        _res = self.usr_search(p_filter)

        # get tree
        for t_item in _res:

            if t_item not in _res_tree:
                t_root = self.__get_root(t_item)
                t_tree = self.__get_tree(t_root)

                _res_tree.extend(t_tree)

        return _res_tree

    def usr_search_tree(self, p_id):
        """
        获取节点及其所有子节点
        :param p_id:
        :return:
        """
        widget = self.usr_search(dict(id=p_id))

        if widget:
            return self.__get_tree(widget[0])
        else:
            return list()

    def usr_search_path(self, p_id):
        """
        查询符合条件的控件,并获取其所有父节点
        :param p_id:
        :return:
        """
        _res_list = []
        _item = self.__session.query(WebWidgetDef).filter(WebWidgetDef.id == p_id).first()

        if _item is not None:
            _res_list = self.usr_search_path(_item.pid)
            _res_list.append(_item)

        return _res_list

    def __get_root(self, p_item):
        """
        :param p_item:
        :return:
        """
        if p_item.pid is None:
            return p_item

        _res = self.__session \
            .query(WebWidgetDef) \
            .filter(WebWidgetDef.id == p_item.pid) \
            .first()

        return self.__get_root(_res)

    def __get_tree(self, p_item):
        """
        :param p_item:
        :return:
        """
        widget_tree = [p_item]
        widget_items = self.__session.query(WebWidgetDef).filter(WebWidgetDef.pid == p_item.id).all()

        for _item in widget_items:
            widget_tree.extend(self.__get_tree(_item))

        return widget_tree

    def usr_add(self, p_data):
        """
        :param p_data:
        :return:
        """
        _node = WebWidgetDef()

        # Create id
        _node.id = gen_id("widget_def")

        # pid
        _node.pid = p_data['pid'] if 'pid' in p_data else None

        # widget_flag
        _node.widget_flag = p_data['widget_flag'] if 'widget_flag' in p_data else ""

        # widget_type
        _node.widget_type = p_data['widget_type'] if 'widget_type' in p_data else ""

        # widget_desc
        _node.widget_desc = p_data['widget_desc'] if 'widget_desc' in p_data else ""

        # batch_desc, comment
        _node.comment = p_data['comment'] if 'comment' in p_data else ""

        # create_time, modify_time
        _node.create_time = datetime.now()
        _node.modify_time = datetime.now()

        try:
            self.__session.add(_node)
            self.__session.commit()
        except:
            raise OrcDatabaseException

        # Modify
        self.usr_update({"id": _node.id,
                         "widget_path": self.usr_get_path(_node.id)})

        return _node

    def __create_no(self):
        """
        Create a no, like batch_no
        :return:
        """
        _no = gen_date_str()
        t_item = self.__session.query(WebWidgetDef).filter(WebWidgetDef.batch_no == _no).first()

        if t_item is not None:
            return self.__create_no()
        else:
            return _no

    def usr_update(self, p_cond):

        for t_id in p_cond:

            if "id" == t_id:
                continue

            _data = None if is_null(p_cond[t_id]) else p_cond[t_id]
            _item = self.__session.query(WebWidgetDef).filter(WebWidgetDef.id == p_cond['id'])
            _item.update({t_id: _data})

        self.__session.commit()

    def usr_delete(self, p_id):

        self.__session.query(WebWidgetDef).filter(WebWidgetDef.id == p_id).delete()
        self.__session.commit()

    # def __del_tree(self, p_id):
    #
    #     def _del(_id):
    #         """
    #         Delete widget detail
    #         :param _id:
    #         :return:
    #         """
    #         _widget_det_list = self.child.usr_search({"widget_id": _id})
    #         _widget_det_ids = dict(list=list(value.id for value in _widget_det_list))
    #
    #         self.child.usr_delete(_widget_det_ids)
    #
    #     try:
    #         # Delete children
    #         _list = self.__session.query(WebWidgetDef.id).filter(WebWidgetDef.pid == p_id).all()
    #
    #         for t_id in _list:
    #             _del(t_id)  # Delete widget detail
    #             self.__del_tree(t_id)  # Delete widget definition
    #
    #         # Delete current item
    #         _del(p_id)  # Delete detail
    #         self.__session \
    #             .query(WebWidgetDef) \
    #             .filter(WebWidgetDef.id == p_id) \
    #             .delete()  # Delete widget definition
    #
    #     except Exception:
    #         # Todo
    #         self.__session.rollback()

    def usr_get_path(self, p_id):

        _no = self.__session.query(WebWidgetDef.widget_flag).filter(WebWidgetDef.id == p_id).first()
        _pid = self.__session.query(WebWidgetDef.pid).filter(WebWidgetDef.id == p_id).first()

        if _no is not None:
            _no = _no[0]
            _pid = _pid[0]

        if _pid is None:
            return _no
        else:
            return "%s.%s" % (self.usr_get_path(_pid), _no)
