# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibCmd import OrcRecordCmd


class DebugService(object):

    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog('view.run.debug.debug_service')

        self.__resource_batch_def = OrcResource('BatchDef')
        self.__resource_case_def = OrcResource('CaseDef')
        self.__resource_item = OrcResource('Item')
        self.__resource_data = OrcResource('Data')

        self.__root_path = list()

    def get_src_ids(self, p_path):
        """
        获取数据id列表,id 列表来源于节点的路径,包括界面显示的节点及当前界面未显示的部分
        :param p_path:
        :return:
        """
        full_path = self.__root_path[:]
        full_path.extend(p_path)

        full_path_ids = [item['id'] for item in full_path]

        return full_path_ids

    def set_root(self, p_root_data):
        """
        设置根节点路径
        :param p_root_data:
        :return:
        """
        root_cmd = OrcRecordCmd(p_root_data)

        if root_cmd.is_batch_type():
            self.__root_path = self.__resource_batch_def.get(
                parameter=dict(type='path', id=root_cmd.id))
        elif root_cmd.is_cases():
            self.__root_path = self.__resource_case_def.get(
                parameter=dict(type='path', id=root_cmd.id))
        else:
            pass
