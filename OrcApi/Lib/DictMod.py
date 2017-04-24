# -*- coding: utf-8 -*-
from OrcLib.LibDatabase import orc_db

from .DictionaryMod import DictionaryMod
from .WidgetTypeMod import WidgetTypeMod
from .WidgetOperationMod import WidgetOperationMod


class DictMod(object):
    """
    Test data management
    """
    __session = orc_db.session

    def __init__(self):

        object.__init__(self)

        self.__model_dictionary = DictionaryMod()
        self.__model_widget_type = WidgetTypeMod()
        self.__model_widget_operation = WidgetOperationMod()

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        if ('TYPE' in p_data) and ('DATA' in p_data):
            dict_type = p_data['TYPE']
            dict_data = p_data['DATA']
        else:
            dict_type = 'dictionary'
            dict_data = p_data

        if 'widget_type' == dict_type:
            return self.__model_widget_type.usr_add(dict_data)
        elif 'widget_operation' == dict_type:
            return self.__model_widget_operation.usr_add(dict_data)
        else:
            return self.__model_dictionary.usr_add(dict_data)

    def usr_delete(self, p_data):
        """
        删除
        :param p_data:
        :return:
        """
        if ('TYPE' in p_data) and ('DATA' in p_data):
            dict_type = p_data['TYPE']
            dict_data = p_data['DATA']
        else:
            dict_type = 'dictionary'
            dict_data = p_data

        if 'widget_type' == dict_type:
            return self.__model_widget_type.usr_delete(dict_data)
        elif 'widget_operation' == dict_type:
            return self.__model_widget_operation.usr_delete(dict_data)
        else:
            return self.__model_dictionary.usr_delete(dict_data)

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        if ('TYPE' in p_data) and ('DATA' in p_data):
            dict_type = p_data['TYPE']
            dict_data = p_data['DATA']
        else:
            dict_type = 'dictionary'
            dict_data = p_data

        if 'widget_type' == dict_type:
            return self.__model_widget_type.usr_update(dict_data)
        elif 'widget_operation' == dict_type:
            return self.__model_widget_operation.usr_update(dict_data)
        else:
            return self.__model_dictionary.usr_update(dict_data)

    def usr_search(self, p_data):
        """
        查询
        :param p_data:
        :return:
        """
        print "+++====", p_data
        if ('TYPE' in p_data) and ('DATA' in p_data):
            dict_type = p_data['TYPE']
            dict_data = p_data['DATA']
        else:
            dict_type = 'dictionary'
            dict_data = p_data
        print dict_type
        if 'widget_type' == dict_type:
            print "AAAA"
            return self.__model_widget_type.usr_search(dict_data)
        elif 'widget_operation' == dict_type:
            return self.__model_widget_operation.usr_search(dict_data)
        else:
            return self.__model_dictionary.usr_search(dict_data)
