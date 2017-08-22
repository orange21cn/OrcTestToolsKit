# coding=utf-8
from LibLog import OrcLog
from LibRunTime import OrcRunTime
from LibType import WebDriverRunningStatusType
from LibType import WebDriverOccupyStatusType
from LibType import RunRecordType


class OrcStatus(OrcRunTime):
    """
    状态基础类,状态存储至实时库
    """
    def __init__(self, p_mod):

        OrcRunTime.__init__(self, p_mod)

        self.__logger = OrcLog("resource.status.%s" % p_mod)

    def _set_status(self, p_flag, p_value):
        """

        :return:
        """
        self.set_value(p_flag, p_value)

    def _get_status(self, p_flag):
        """
        设置进度
        :return:
        """
        return self.get_value(p_flag)


class RecordStatus(object):
    """
    运行状态
    """
    def __init__(self, p_status=None):

        object.__init__(self)

        self.status = RunRecordType.NEW

        self.set_status(p_status)

    def set_status(self, p_status):
        """
        设置状态
        :param p_status:
        :return:
        """
        if p_status in RunRecordType.all():
            self.status = p_status

    def plus(self, p_status):
        """
        叠加一个状态
        :param p_status:
        :type p_status: RecordStatus
        :return:
        """
        if self.is_new():
            self.status = p_status.status

        elif self.is_waiting():
            self.status = p_status.status

        elif self.is_running():
            self.status = p_status.status

        elif self.is_pass() and p_status.is_fail():
            self.set_fail()

        else:
            pass

    def get_status(self):
        """
        获取状态
        :return:
        """
        return self.status

    def set_new(self):
        """
        设置为新建
        :return:
        """
        self.status = RunRecordType.NEW

    def is_new(self):
        """
        是否新建
        :return:
        """
        return self.status == RunRecordType.NEW

    def set_waiting(self):
        """
        设置为等待
        :return:
        """
        self.status = RunRecordType.WAITING

    def is_waiting(self):
        """
        是否等待
        :return:
        """
        return self.status == RunRecordType.WAITING

    def set_running(self):
        """
        设置为运行
        :return:
        """
        self.status = RunRecordType.RUNNING

    def is_running(self):
        """
        是否运行
        :return:
        """
        return self.status == RunRecordType.RUNNING

    def set_pass(self):
        """
        设置为通过
        :return:
        """
        self.status = RunRecordType.PASS

    def is_pass(self):
        """
        是否通过
        :return:
        """
        return self.status == RunRecordType.PASS

    def set_fail(self):
        """
        设置为失败
        :return:
        """
        self.status = RunRecordType.FAIL

    def is_fail(self):
        """
        是否失败
        :return:
        """
        return self.status == RunRecordType.FAIL


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
        result = self.__run_time.get_value('RUN_STATUS')

        if result is None:
            return False
        else:
            return bool(int(result))

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


class OrcDriverStatus(OrcStatus):

    def __init__(self, p_name):

        OrcStatus.__init__(self, 'DRIVER')

        # 驱动名称
        self._name = p_name

        # 占用状态标识,session 表示占用
        self._occupy_status_flag = "%s.OCCUPY" % self._name

        # 运行状态标识
        self._running_status_flag = "%s-RUNNING" % self._name

    def _set_running(self, p_value):
        """
        设置数据
        :param p_value:
        :return:
        """
        if p_value in WebDriverRunningStatusType.all():
            self._set_status(self._running_status_flag, p_value)

    def _get_running(self):
        """
        获取数据
        :return:
        """
        return self._get_status(self._running_status_flag)

    def _set_occupy(self, p_value):
        """
        设置占用状态
        :param p_value:
        :return:
        """
        self._set_status(self._occupy_status_flag, p_value)

    def _get_occupy(self):
        """
        获取占用状态
        :return:
        """
        return self._get_status(self._occupy_status_flag)

    def get_session(self):
        """
        获取 session
        :return:
        """
        occupy_status = self._get_occupy()
        if occupy_status in WebDriverOccupyStatusType.all():
            return None
        else:
            return occupy_status

    def set_waiting(self):
        """
        设置为等待状态
        :return:
        """
        self._set_occupy(WebDriverOccupyStatusType.WAITING)

    def is_waiting(self):
        """
        是否等待状态
        :return:
        """
        return self._get_occupy() == WebDriverOccupyStatusType.WAITING

    def set_occupy(self, p_session):
        """
        设置为占用状态
        :param p_session:
        :return:
        """
        self._set_occupy(p_session)

    def is_occupy(self):
        """
        是否占用状态
        :return:
        """
        return self._get_occupy() != WebDriverOccupyStatusType.WAITING

    def set_idle(self):
        """
        设置为空闲
        :return:
        """
        self._set_running(WebDriverRunningStatusType.IDLE)

    def is_idle(self):
        """
        是否空闲
        :return:
        """
        return self._get_running() == WebDriverRunningStatusType.IDLE

    def set_busy(self):
        """
        设置为空闲
        :return:
        """
        self._set_running(WebDriverRunningStatusType.BUSY)

    def is_busy(self):
        """
        当前是否空闲
        :return:
        """
        return self._get_running() == WebDriverRunningStatusType.IDLE

    def set_error(self):
        """
        设置为出错状态
        :return:
        """
        self._set_running(WebDriverRunningStatusType.ERROR)

    def is_error(self):
        """
        当前是否出错
        :return:
        """
        return self._get_running() == WebDriverRunningStatusType.IDLE
