# coding=utf-8
from OrcLib.LibNet import OrcHttpNewResource


class Runtime(object):
    """

    """
    def __init__(self, p_mod):

        object.__init__(self)

        self.__mod = p_mod
        self.__resource = OrcHttpNewResource("RunTime")

    def add_value(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        data = dict(module=self.__mod)
        data.update(p_data)
        return self.__resource.post(data)

    def get_value(self, p_flag):
        """
        获取数据
        :param p_flag:
        :return:
        """
        cond = dict(module=self.__mod, data_flag=p_flag)
        result = self.__resource.get(cond)

        return None if not result else result[0]["data_value"]

    def get_values(self, p_flag):
        """
        获取多条数据
        :param p_flag:
        :return:
        """
        cond = dict(module=self.__mod, data_flag=p_flag)
        result = self.__resource.get(cond)

        return None if not result else [item["data_value"] for item in result]

    def set_value(self, p_flag, p_value, p_index=None):
        """
        设置数据,如果不存在就新增一个,数据有多个时只入第一个
        :param p_index:
        :param p_flag:
        :param p_value:
        :return:
        """
        # 生成查询条件
        cond = dict(module=self.__mod, data_flag=p_flag)
        if p_index is not None:
            cond["data_index"] = p_index

        # 判断数据存在,如果存在找到 id
        data_item = self.__resource.get(cond)
        data_id = None if data_item is None else data_item[0]["id"]

        # 设置值
        if data_id is not None:
            self.__resource.set_path(data_id)
            result = self.__resource.put(dict(data_value=p_value))
        else:
            cond["data_value"] = p_value
            result = self.__resource.post(cond)

        return result

    def del_value(self, p_flag, p_index=None):
        """
        删除数据
        :param p_index:
        :type p_index: int
        :param p_flag:
        :return:
        """
        # 查找数据
        cond = dict(module=self.__mod, data_flag=p_flag)
        data_list = self.__resource.get(cond)

        # 获取 id list
        data_id_list = None if data_list is None else [item["id"] for item in data_list]

        # 不存在合适的对象
        if data_id_list is None:
            return False

        # 只删除一条的情况
        if p_index is not None:

            # index 超出范围
            if p_index < len(data_id_list):
                data_id = data_id_list[p_index]
                self.__resource.set_path(data_id)
                return self.__resource.delete()
            else:
                return False

        # 删除符合条件全部数据
        else:
            return self.__resource.delete(data_id_list)
