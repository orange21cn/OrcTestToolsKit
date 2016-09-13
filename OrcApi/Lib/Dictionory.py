# -*- coding: utf-8 -*-
from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import orc_db


class DictHandle():
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):
        pass

    def get_dict_text(self, p_flag):
        """
        :param p_flag: {flag, value}
        :return: text
        """
        _res = self.__session.query(LibDictionary).\
            filter(LibDictionary.dict_flag == p_flag["flag"]).\
            filter(LibDictionary.dict_value == p_flag["value"]).\
            first()

        return _res.dict_text
