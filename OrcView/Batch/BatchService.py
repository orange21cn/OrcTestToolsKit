# coding=utf-8
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibNet import OrcResource
from OrcLib.LibApi import connect_list


class BatchDefService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_batch_def = OrcResource("BatchDef")
        self.__resource_run_def = OrcHttpResource("RunDef")

    def usr_add(self, p_data):
        """
        增加
        :param p_data:
        :return:
        """
        msg = self.__resource_batch_def.post(parameter=p_data)
        node = msg.data if msg is not None else None

        return None if node is None else dict(id=node["id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        msg = self.__resource_batch_def.delete(parameter=p_list)

        return None if msg is None else msg.status

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        msg = self.__resource_batch_def.put(path=p_data["id"], parameter=p_data)

        return None if msg is None else msg.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        cond = dict(type="all")
        cond.update(p_cond)
        msg = self.__resource_batch_def.get(parameter=cond)

        return None if msg is None else msg.data

    def add_to_run(self, p_id):
        """
        加入运行列表
        :param p_id:
        :return:
        """
        cond = dict(id=p_id, run_def_type="BATCH")
        self.__resource_run_def.post(cond)


class BatchDetService(object):

    def __init__(self):

        object.__init__(self)

        self.__resource_batch_det = OrcHttpResource("BatchDet")
        self.__resource_case_def = OrcHttpResource("CaseDef")

    def usr_add(self, p_data):
        """
        增加,将多条记录转换为单条
        :param p_data:
        :return:
        """
        batch_id = p_data["batch_id"]

        for _case_id in p_data["case"]:
            self.__resource_batch_det.post(dict(batch_id=batch_id, case_id=_case_id))

        return dict(batch_id=batch_id)

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        return self.__resource_batch_det.delete(p_list)

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        self.__resource_batch_det.set_path(p_data["id"])
        return self.__resource_batch_det.put(p_data)

    def usr_search(self, p_cond):
        """
        查询,查询batch及case并连接数据
        :param p_cond:
        :return:
        """
        # 查询 batch_det 列表
        batch_det_list = self.__resource_batch_det.get(p_cond)

        # case_det id 列表
        case_def_id_list = [batch_det["case_id"] for batch_det in batch_det_list]

        # case_def 列表
        case_def_list = self.__resource_case_def.get(dict(id=case_def_id_list))

        # 连接 list 并返回
        return connect_list(batch_det_list, case_def_list, "case_id")
