# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibStatus import OrcRunStatus


from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibControl import ControlBase
from OrcLib.LibCmd import OrcRecordCmd


class RunDetControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'RunDet')


class RunDetModel(ModelTree):

    def __init__(self):

        ModelTree.__init__(self, 'RunDet')

        self.__logger = LogClient()

        self.__resource_run_det = OrcResource("RunDet")
        self.__resource_run = OrcResource("Run")

        self.__run_status = OrcRunStatus()

        self.basic_checkable()

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

    def service_get_child_list(self, p_id):
        """
        获取子节点列表
        :param p_id:
        :return:
        """
        return self._data_struct.get_children_list(p_id)

    def service_get_item_list(self, p_id):
        """
        获取 item 列表
        :param p_id:
        :return:
        """
        result = list()

        children = self.service_get_child_list(p_id)
        for _child_data in children:
            _child = OrcRecordCmd(_child_data)

            if _child.is_item_type():
                result.append(_child_data)

        return result

    def service_get_path(self, p_id):
        """
        获取路径
        :param p_id:
        :return:
        """
        return self._data_struct.get_path(p_id)
