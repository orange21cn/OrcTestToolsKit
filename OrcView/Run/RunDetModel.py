# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibRunTime import OrcRunStatus


from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTree import ModelTree


class RunDetModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self, 'RunDet')

        self.__logger = LogClient()

        self.__resource_run_det = OrcResource("RunDet")
        self.__resource_run = OrcResource("Run")

        self.__run_status = OrcRunStatus()

        self.checkable()

    def service_search(self, p_path):
        """
        查询
        :param p_path:
        :return:
        """
        result = self.__resource_run_det.get(parameter=p_path)

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询测试清单", self.__logger):
            return list()

        # 打印成功信息
        ResourceCheck.result_success(u"查询测试清单", self.__logger)

        return result.data

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        pass

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        pass

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        pass

    def service_run(self, p_path):
        """

        :param p_path:
        :return:
        """
        result = self.__resource_run.put(p_path)

        # 检查结果
        if not ResourceCheck.result_status(result, u"执行测试", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"执行测试", self.__logger)

        return result.status

    def service_item_nums(self, p_node=None):
        """

        :param p_node:
        :return:
        """
        count = 0

        if p_node is None:
            node = self._root
        else:
            node = p_node

        if node.content is not None:
            count = 1

        if node.children:
            for child in node.children:
                count += self.service_item_nums(child)

        return count

    def service_get_usr_status(self):
        """
        获取执行状态
        :return:
        """
        return self.__run_status.status

    def service_get_steps(self):
        """

        :return:
        """
        return self.__run_status.get_steps()
