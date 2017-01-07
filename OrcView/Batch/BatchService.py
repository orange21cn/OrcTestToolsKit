# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibApi import connect_list
from OrcView.Lib.LibMain import LogClient


class BatchDefService(object):

    def __init__(self):

        object.__init__(self)

        self.__logger = LogClient()

        self.__resource_batch_def = OrcResource("BatchDef")
        self.__resource_run_def = OrcResource("RunDef")

    def usr_add(self, p_data):
        """
        增加
        :param p_data:
        :return:
        """
        msg = self.__resource_batch_def.post(parameter=p_data)

        if msg is None:
            self.__logger.put_error(u"新增计划失败, 网络连接失败.")
            return dict()

        if not msg.status:
            self.__logger.put_error("新增计划失败, %s" % msg.message)
            return dict()

        self.__logger.put_message(u"新增计划成功")

        return dict(id=msg.data["id"])

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        msg = self.__resource_batch_def.delete(parameter=p_list)

        if msg is None:
            self.__logger.put_error(u"删除计划失败, 网络连接失败.")
            return False

        if not msg.status:
            self.__logger.put_error(u"删除计划失败, %s" % msg.message)
            return False

        self.__logger.put_message(u"删除计划成功")

        return msg.status

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        msg = self.__resource_batch_def.put(path=p_data["id"], parameter=p_data)

        if msg is None:
            self.__logger.put_error(u"更新计划失败, 网络连接失败.")
            return False

        if not msg.status:
            self.__logger.put_error(u"更新计划失败, %s" % msg.message)
            return False

        self.__logger.put_message(u"更新计划成功")

        return msg.status

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        cond = dict(type="all")
        cond.update(p_cond)

        msg = self.__resource_batch_def.get(parameter=cond)

        if msg is None:
            self.__logger.put_error(u"查询计划失败, 网络连接失败.")
            return False

        if not msg.status:
            self.__logger.put_error(u"查询计划失败, %s" % msg.message)
            return False

        self.__logger.put_message(u"查询计划成功")

        return msg.data

    def add_to_run(self, p_id):
        """
        加入运行列表
        :param p_id:
        :return:
        """
        cond = dict(id=p_id, run_def_type="BATCH")
        msg = self.__resource_run_def.post(parameter=cond)

        if msg is None:
            self.__logger.put_error(u"添加至运行失败, 网络连接失败.")
            return False

        if not msg.status:
            self.__logger.put_error(u"添加至运行失败, %s" % msg.message)
            return False

        self.__logger.put_message(u"添加至运行成功")

        return True


class BatchDetService(object):

    def __init__(self):

        object.__init__(self)

        self.__logger = LogClient()

        self.__resource_batch_det = OrcResource("BatchDet")
        self.__resource_case_def = OrcResource("CaseDef")

    def usr_add(self, p_data):
        """
        增加,将多条记录转换为单条
        :param p_data:
        :return:
        """
        batch_id = p_data["batch_id"]

        for _case_id in p_data["case"]:

            msg = self.__resource_batch_det.post(parameter=dict(batch_id=batch_id, case_id=_case_id))

            if msg is None:
                self.__logger.put_error(u"添加用例失败, 网络连接失败.")
                return dict()

            if not msg.status:
                self.__logger.put_error(u"添加用例失败, %s" % msg.message)
                return dict()

        self.__logger.put_message(u"添加用例成功")

        return dict(batch_id=batch_id)

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        msg = self.__resource_batch_det.delete(parameter=p_list)

        if msg is None:
            self.__logger.put_error(u"删除用例失败, 网络连接失败.")
            return False

        if not msg.status:
            self.__logger.put_error(u"删除用例失败, %s" % msg.message)
            return False

        self.__logger.put_message(u"删除用例成功")

        return msg.status

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        msg = self.__resource_batch_det.put(path=p_data["id"], parameter=p_data)

        if msg is None:
            self.__logger.put_error(u"更新用例列表失败, 网络连接失败.")
            return False

        if not msg.status:
            self.__logger.put_error(u"更新用例列表失败, %s" % msg.message)
            return False

        self.__logger.put_message(u"更新用例列表成功")

        return msg.status

    def usr_search(self, p_cond):
        """
        查询,查询batch及case并连接数据
        :param p_cond:
        :return:
        """
        # 查询 batch_det 列表
        msg = self.__resource_batch_det.get(parameter=p_cond)

        if msg is None:
            self.__logger.put_error(u"查询用例列表失败, 网络连接失败.")
            return list()

        if not msg.status:
            self.__logger.put_error(u"查询用例列表失败, %s" % msg.message)
            return list()

        batch_det_list = msg.data

        # case_det id 列表
        case_def_id_list = [batch_det["case_id"] for batch_det in batch_det_list]
        print case_def_id_list

        # case_def 列表
        msg = self.__resource_case_def.get(parameter=dict(id=case_def_id_list))
        print msg

        if msg is None:
            self.__logger.put_error(u"查询用例列表失败, 网络连接失败.")
            return list()

        if not msg.status:
            self.__logger.put_error(u"查询用例列表失败, %s" % msg.message)
            return list()

        case_def_list = msg.data
        print case_def_list

        # 连接 list 并返回
        res = connect_list(batch_det_list, case_def_list, "case_id")
        print res
        return res
