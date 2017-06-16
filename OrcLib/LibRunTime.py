# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck


class OrcRunTime(object):
    """

    """
    def __init__(self, p_mod):

        object.__init__(self)

        self.__logger = OrcLog('basic.run_time')

        self.__mod = p_mod
        self.__resource = OrcResource('RunTime')

    def add_value(self, p_flag, p_data):
        """
        新增
        :param p_flag:
        :param p_data:
        :type p_data:
        :return:
        """
        data = dict(module=self.__mod, data_flag=p_flag, data_value=p_data)

        result = self.__resource.post(parameter=data)

        if not ResourceCheck.result_status(result, u'新增实时数据', self.__logger):
            return False

        return True

    def get_value(self, p_flag):
        """
        获取数据
        :param p_flag:
        :return:
        """
        cond = dict(module=self.__mod, data_flag=p_flag)
        result = self.__resource.get(parameter=cond)

        if not ResourceCheck.result_status(result, u'获取实时数据', self.__logger):
            return None

        if not result.data:
            self.__logger.error(u"获取实时数据出错,取值为: %s" % result.data)
            return None
        else:
            return result.data[0]["data_value"]

    def get_values(self, p_flag):
        """
        获取多条数据
        :param p_flag:
        :return:
        """
        cond = dict(module=self.__mod, data_flag=p_flag)

        result = self.__resource.get(parameter=cond)

        if not ResourceCheck.result_status(result, u'获取实时数据', self.__logger):
            return list()

        return {item['data_index']: item["data_value"] for item in result.data}

    def set_value(self, p_flag, p_value, p_index=None):
        """
        设置数据,如果不存在就新增一个,数据有多个时只设置第一个
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
        data_item = self.__resource.get(parameter=cond)
        data_id = None if not data_item.data else data_item.data[0]["id"]

        # 设置值
        if data_id is not None:
            result = self.__resource.put(path=data_id, parameter=dict(data_value=p_value))

            if not ResourceCheck.result_status(result, u'设置实时数据', self.__logger):
                return False

            result = result.status

        else:
            result = self.add_value(p_flag, p_value)

        return result

    def del_value(self, p_flag=None, p_index=None):
        """
        删除数据
        :param p_index:
        :param p_flag:
        :return:
        """
        # 查询条件
        cond = dict(module=self.__mod)

        if p_flag is not None:
            cond['data_flag'] = p_flag

        if p_index is not None:
            cond['data_index'] = p_index

        # 查询
        result = self.__resource.get(parameter=cond)

        if not ResourceCheck.result_status(result, u'获取实时数据', self.__logger):
            return False

        # 获取列表
        data_ids = [item['id'] for item in result.data]

        # 删除
        result = self.__resource.delete(parameter=data_ids)

        if not ResourceCheck.result_status(result, u'删除实时数据', self.__logger):
            return False

        return True


class OrcRunStatus(object):
    """

    """
    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog("resource.Run.run.service")
        self.__run_time = OrcRunTime("RUN")

    @property
    def process(self):
        """
        当前的运行进度
        :return:
        """
        return self.__run_time.get_value('RUN_PROCESS')

    @process.setter
    def process(self, value):
        """
        设置进度
        :return:
        """
        self.__run_time.set_value('RUN_PROCESS', value)

    @property
    def status(self):
        """
        当前实际状态
        :return:
        :return:
        """
        return self.__run_time.get_value('RUN_STATUS')

    @status.setter
    def status(self, p_status):
        """
        设置状态
        :return:
        """
        self.__run_time.set_value('RUN_STATUS', p_status)

    @property
    def director(self):
        """
        指示状态
        :return:
        """
        return self.__run_time.get_value('RUN_DIRECTOR')

    @director.setter
    def director(self, p_director):
        """
        设置指示状态
        :return:
        """
        self.__run_time.set_value('RUN_DIRECTOR', p_director)

    def step_forward(self):
        """
        下一步,进度加 1
        :return:
        """
        prc = self.process

        if prc is None:
            prc = 1
        else:
            prc = int(self.process) + 1

        self.process = prc

    def step_message(self, p_message):
        """
        输出执行完的步骤信息
        :param p_message:
        :return:
        """
        self.step_forward()

        self.__run_time.add_value('RUN_STEP', p_message)

    def get_steps(self):
        """
        获取步骤信息
        :return:
        """
        result = self.__run_time.get_values('RUN_STEP')

        for _index in result:
            self.__run_time.del_value('RUN_STEP', _index)

        return result

    def clean(self):
        """
        清空数据
        :return:
        """
        self.__run_time.del_value()
