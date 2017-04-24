# -*- coding: utf-8 -*-
from OrcLib.LibDatabase import LibWidgetType
from OrcLib.LibDatabase import orc_db
from OrcLib.LibDatabase import gen_id

from OrcLib.LibException import OrcDatabaseException


class WidgetTypeMod(object):
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        object.__init__(self)

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        _node = LibWidgetType()

        # Create id
        _node.id = gen_id("dict")

        # type_order
        _node.dict_flag = p_data['type_order'] if 'type_order' in p_data else None

        # type_mode
        _node.dict_order = p_data['type_mode'] if 'type_mode' in p_data else None

        # type_name
        _node.dict_value = p_data['type_name'] if 'type_name' in p_data else None

        # type_text
        _node.dict_text = p_data['type_text'] if 'type_text' in p_data else None

        # type_desc
        _node.dict_desc = p_data['type_desc'] if 'type_desc' in p_data else None

        try:
            self.__session.add(_node)
            self.__session.commit()
        except Exception:
            raise OrcDatabaseException

        return _node

    def usr_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        try:
            self.__session.query(LibWidgetType).filter(LibWidgetType.id == p_id).delete()
            self.__session.commit()
        except Exception:
            raise OrcDatabaseException

        return True

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        try:
            for _key in p_data:

                if "id" == _key:
                    continue

                _item = self.__session.query(LibWidgetType).filter(LibWidgetType.id == p_data["id"])
                _item.update({_key: (None if not p_data[_key] else p_data[_key])})

            self.__session.commit()

        except Exception:
            raise OrcDatabaseException

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__session.query(LibWidgetType)

        if 'id' in p_cond:
            result = result.filter(LibWidgetType.id == p_cond['id'])

        if 'type_mode' in p_cond:
            result = result.filter(LibWidgetType.type_mode == p_cond['type_mode'])

        if 'type_name' in p_cond:
            result = result.filter(LibWidgetType.type_name == p_cond['type_name'])

        if 'type_text' in p_cond:
            result = result.filter(LibWidgetType.type_text == p_cond['type_text'])

        return result.all()
