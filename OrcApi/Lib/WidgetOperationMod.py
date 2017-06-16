# -*- coding: utf-8 -*-
from OrcLib.LibDatabase import LibWidgetOperation
from OrcLib.LibDatabase import orc_db
from OrcLib.LibDatabase import gen_id

from OrcLib.LibException import OrcDatabaseException


class WidgetOperationMod(object):
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
        _node = LibWidgetOperation()

        # Create id
        _node.id = gen_id("widget_operation")

        # type_name
        _node.type_name = p_data['type_name'] if 'type_name' in p_data else None

        # ope_order
        _node.ope_order = p_data['ope_order'] if 'ope_order' in p_data else None

        # ope_name
        _node.ope_name = p_data['ope_name'] if 'ope_name' in p_data else None

        # ope_text
        _node.ope_text = p_data['ope_text'] if 'ope_text' in p_data else None

        # ope_desc
        _node.dict_desc = p_data['ope_desc'] if 'ope_desc' in p_data else None

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
            self.__session.query(LibWidgetOperation).filter(LibWidgetOperation.id == p_id).delete()
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

                _item = self.__session.query(LibWidgetOperation).filter(LibWidgetOperation.id == p_data["id"])
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
        cond = p_cond if p_cond else dict()

        result = self.__session.query(LibWidgetOperation)

        if 'id' in cond:

            # 查询支持多 id
            if isinstance(cond["id"], list):
                result = result.filter(LibWidgetOperation.id.in_(cond['id']))
            else:
                result = result.filter(LibWidgetOperation.id == cond['id'])

        if 'type_name' in p_cond:

            # 查询支持多 id
            if isinstance(cond["type_name"], list):
                result = result.filter(LibWidgetOperation.type_name.in_(cond['type_name']))
            else:
                result = result.filter(LibWidgetOperation.type_name == cond['type_name'])

        if 'ope_name' in p_cond:
            result = result.filter(LibWidgetOperation.ope_name == p_cond['ope_name'])

        if 'ope_text' in p_cond:
            result = result.filter(LibWidgetOperation.ope_text == p_cond['ope_text'])

        return result.all()
