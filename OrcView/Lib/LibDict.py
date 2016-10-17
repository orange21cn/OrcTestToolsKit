# coding=utf-8
from OrcLib.LibDatabase import orc_db
from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import LibWidgetType
from OrcLib.LibDatabase import LibWidgetOperation


class LibDict:

    def __init__(self):

        self.__dict = orc_db.session.query(LibDictionary)
        self.__type = orc_db.session.query(LibWidgetType)
        self.__ope = orc_db.session.query(LibWidgetOperation)

    def get_dict(self, p_flg, p_value=None):
        """
        :param p_value:
        :param p_flg:
        :type p_flg: str
        :return: 返回数组
        :rtype: LibDictionary
        """
        _res = self.__dict
        _res = _res.filter(LibDictionary.dict_flag == p_flg)

        if p_value is not None:
            _res = _res.filter(LibDictionary.dict_value == p_value)

        _res = _res.order_by(LibDictionary.dict_order)

        return _res.all()

    def get_widget_type(self, p_id=None, p_name=None):
        """
        :param p_id:
        :param p_name:
        :return:
        """
        _res = self.__type

        # 根据 id 查找
        if p_id is not None:
            _res = _res.filter(LibWidgetType.id == p_id)

        # 根据 name 查找
        if p_name is not None:
            _res = _res.filter(LibWidgetType.type_name == p_name)

        _res = _res.order_by(LibWidgetType.type_order)

        # 没有参数时查找所有
        if p_id is None and p_name is None:
            _res = _res.all()
        else:
            _res = _res.first()

        return _res

    def get_widget_operation(self, p_type_name):
        """
        :param p_type_name:
        :return:
        """
        _res = self.__ope\
            .filter(LibWidgetOperation.type_name == p_type_name)\
            .order_by(LibWidgetOperation.ope_order)

        return _res.all()
