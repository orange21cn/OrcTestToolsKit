# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcView.Lib.LibView import ResourceCheck


class DataService:

    def __init__(self):
        self.__resource_data = OrcResource("Data")

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        result = self.__resource_data.post(parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"增加数据"):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"增加数据")

        return dict(id=result.data["id"])

    def usr_delete(self, p_cond):
        """
        删除
        :param p_cond:
        :return:
        """
        result = self.__resource_data.delete(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除数据"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除数据")

        return result.status

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        result = self.__resource_data.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除数据"):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除数据")

        return result.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource_data.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除数据"):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"删除数据")

        return result.data
