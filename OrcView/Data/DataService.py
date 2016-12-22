# coding=utf-8
from OrcLib.LibNet import OrcHttpResource


class DataService:

    def __init__(self):
        self.__resource_data = OrcHttpResource("Data")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        data_data = self.__resource_data.post(p_data)
        return dict(id=data_data["id"])

    def usr_delete(self, p_cond):
        """
        删除
        :param p_cond:
        :return:
        """
        self.__resource_data.delete(p_cond)

    def usr_update(self, p_data):
        """
        更新
        :param p_cond:
        :return:
        """
        self.__resource_data.set_path(p_data["id"])
        self.__resource_data.put(p_data)

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        return self.__resource_data.get(p_cond)
