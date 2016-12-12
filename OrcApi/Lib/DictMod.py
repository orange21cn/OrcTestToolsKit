# -*- coding: utf-8 -*-
from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import orc_db
from OrcLib.LibDatabase import gen_id

from OrcLib.LibException import OrcDatabaseException


class DictMod(object):
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        object.__init__(self)

    def mod_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        _node = LibDictionary()

        # Create id
        _node.id = gen_id("dict")

        # batch_no
        _node.dict_flag = p_data['dict_flag'] if 'dict_flag' in p_data else None

        # batch_type
        _node.dict_order = p_data['dict_order'] if 'dict_order' in p_data else None

        # pid
        _node.dict_value = p_data['dict_value'] if 'dict_value' in p_data else None

        # batch_name
        _node.dict_text = p_data['dict_text'] if 'dict_text' in p_data else None

        # batch_desc, comment
        _node.dict_desc = p_data['dict_desc'] if 'dict_desc' in p_data else None

        try:
            self.__session.add(_node)
            self.__session.commit()
        except Exception:
            raise OrcDatabaseException

        return _node

    def mod_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        try:
            self.__session.query(LibDictionary).filter(LibDictionary.id == p_id).delete()
            self.__session.commit()
        except Exception:
            raise OrcDatabaseException

        return True

    def mod_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        try:
            for _key in p_data:

                if "id" == _key:
                    continue
                print p_data
                _item = self.__session.query(LibDictionary).filter(LibDictionary.id == p_data["id"])
                print {_key: (None if not p_data[_key] else p_data[_key])}
                _item.update({_key: (None if not p_data[_key] else p_data[_key])})

            self.__session.commit()

        except Exception:
            raise OrcDatabaseException

    def mod_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__session.query(LibDictionary)

        if 'id' in p_cond:
            result = result.filter(LibDictionary.id == p_cond['id'])

        if 'dict_flag' in p_cond:
            result = result.filter(LibDictionary.dict_flag == p_cond['dict_flag'])

        if 'dict_value' in p_cond:
            result = result.filter(LibDictionary.dict_value == p_cond['dict_value'])

        if 'dict_text' in p_cond:
            result = result.filter(LibDictionary.dict_text == p_cond['dict_text'])

        return result.all()
