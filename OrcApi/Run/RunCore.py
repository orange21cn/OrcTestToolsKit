# coding=utf-8
import json
import os
import re

from OrcLib import get_config
from OrcLib.LibCmd import OrcCmd
from OrcLib.LibCmd import OrcDriverCmd
from OrcLib.LibCmd import OrcRecordCmd
from OrcLib.LibCmd import OrcSysCmd
from OrcLib.LibCmd import WebCmd
from OrcLib.LibCmd import DataCmd
from OrcLib.LibDriver import DriverSession
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibNet import OrcDriverResource
from OrcLib.LibProgram import OrcFactory
from OrcLib.LibStatus import OrcRunStatus
from OrcLib.LibStatus import OrcDriverStatus
from OrcLib.LibThreadPool import ThreadPool
from OrcLib.LibThreadPool import WorkRequest
from OrcLib.LibThreadPool import NoResultsPending
from OrcLibFrame.LibData import OrcDataClient

from OrcLib.LibType import RunRecordType
from RunData import RunData
from RunLog import RunLog
from RunService import RunCoreService


class RunCore(object):

    def __init__(self):

        object.__init__(self)

        # Log 普通日志
        self._logger = OrcLog("resource.run.run_core")

        # service
        self._service_core = RunCoreService()

        # 测试记录
        self._recoder = Recoder()

        # 测试 log
        self._run_logger = RunLog()

        # 用例分配器
        self._allot = CaseAllot()

        # 临时保存数据标识(如图片名称),用于标识同一目录下不同的步骤项
        self._data_flag = ""

        self._status = OrcRunStatus()

        self.thread = None

    def stop(self):
        """
        终止
        :return:
        """
        self._status.director = False

    def get_status(self):
        """
        获取状态
        :return:
        """
        return self._status.status

    def start(self, p_para):
        """
        读取运行记录文件并逐条执行
        :param p_para: {PATH, PARA, ...}
        :return:
        """
        # Todo 如果所有驱动被占用,显示驱动忙
        # if self.__status.status:
        #     return False, u'驱动忙'

        # self.__status.director = True
        parameter = OrcFactory.create_default_dict(p_para)
        run_path = parameter.value('PATH')
        run_para = parameter.value('PARA')

        self._recoder.set_path(run_path)

        self._allot.init(self._recoder.get_rec_file())

        main = ThreadPool(1)
        for _steps in self._allot.cases():

            _home = self._recoder.get_run_home()
            _current_path = self._allot.get_current_path()

            for i in _current_path:

                _home = os.path.join(_home, i['flag'])

            runner = CaseRunner(_current_path, _home)
            runner.set_parameter(run_para)

            req = WorkRequest(runner.run, p_args=[_steps], p_kwds={}, p_callback=self.set_status)

            main.put_request(req)

        while True:
            try:
                main.poll()
            except NoResultsPending:
                self._logger.info('Finished all cases...')
                break

        main.stop()

    def set_status(self, p_req, p_res):
        """
        设置状态
        :param p_req:
        :param p_res:
        :return:
        """
        for _cmd in p_res:
            assert isinstance(_cmd, OrcRecordCmd)
            self._allot.update_status(_cmd)


class CaseRunner(object):
    """

    """
    def __init__(self, p_case_path, p_folder):

        object.__init__(self)

        self.__logger = OrcLog("resource.run.run_core")

        # 驱动状态库 {key, status},包含配置文件中所有的驱动
        self._driver_lib = DriverLib()

        # sessions
        self._sessions = DriverSession()

        # driver key
        self._key = None

        # driver resource, {key, res}
        # self._resources = dict()

        # command
        self._command = OrcCmd()
        self._sys_command = OrcSysCmd()
        self._driver_command = OrcDriverCmd

        # 运行日志记录
        self._run_logger = RunLog()

        # 当前  case 路径
        self._case_path = p_case_path
        self._case_folder = p_folder

        # service
        self._service_core = RunCoreService()

        # 数据标识
        self._data_flag = ''

        # 环境
        self._env = None

        # 运行所需其他参数
        self._parameter = dict()

        # 数据获取接口
        self._data_client = OrcDataClient()

        # 当前函数 id, 用于标识函数步骤, 非函数步骤时为 None
        self.__func_step = None

    def set_parameter(self, p_para):
        """
        设置参数
        :param p_para:
        :return:
        """
        self._parameter.update(p_para)

    def run(self, p_steps):
        """
        运用
        :param p_steps:
        :return:
        """
        if 'env' not in self._parameter:
            return

        # 终止 Todo

        # 申请一台驱动服务器
        self.apply()

        if self._key is None:
            self.__logger.error("Apply a driver server failed.")
            return

        result = self._run_case(p_steps)

        # 释放服务器
        self.release()

        return result

    def _run_case(self, p_steps):
        """
        :param p_steps: [step] 步骤
        :return:
        """
        # 生成 case 运行记录目录
        self._run_logger.set_case_folder(self._case_folder)

        result_list = []

        step_result = True

        # 执行步骤
        for _step in p_steps:

            step_cmd = OrcRecordCmd(_step['content'])

            self._data_flag = step_cmd.flag
            self._run_logger.run_begin(step_cmd)

            if step_cmd.is_func_step():

                self.__func_step = step_cmd.id

                for _sub_step in _step['children']:
                    sub_stp_cmd = OrcRecordCmd(_sub_step['content'])

                    self._data_flag = "%s:%s" % (self._data_flag, sub_stp_cmd.flag)
                    _func_result = self._run_case(_sub_step['children'])
                    result_list.extend(_func_result)

                    # 函数的最后一个步骤结果表示函数步骤的状态
                    step_result = _func_result[-1].status.get_status() == RunRecordType.PASS

                    if not step_result:
                        break

                self.__func_step = None
            else:
                # 将步骤加入路径
                _step_path = self._case_path[:]
                _step_path.append(_step['content'])

                for _item in _step['children']:

                    # 将 item 加入路径
                    _item_path = _step_path[:]
                    _item_path.append(_item['content'])

                    # item cmd
                    _item_cmd = OrcRecordCmd(_item['content'])

                    self._data_flag = "%s_%s" % (self._data_flag, _item_cmd.flag)

                    # 记录步骤开始
                    self._run_logger.run_begin(_item_cmd)

                    # 运行
                    _result = self.__run_item(_item_path)
                    step_result = step_result and _result

                    # 更新状态
                    _item_cmd.status.set_status(RunRecordType.from_bool(_result))
                    result_list.append(_item_cmd)

                    # 记录结束
                    self._run_logger.run_end(_item_cmd.status.status)

                    if not step_result:
                        break

            if not step_result:
                break

        return result_list

    def __run_item(self, p_item_path):
        """
        {'status': 'WAITING',
         'flag': '20161028153349',
         'run_det_type': 'BATCH_SUIT',
         'pid': None, 'id': '1000000001',
         'desc': 'BATCH_001'}
        :param p_item_path:
        :return:
        """
        _result = True

        # 执行该 list 的最后一项,最后一项为 item, 其他为路径用于数据查找
        item_id = p_item_path[len(p_item_path) - 1]["id"]
        item = self._service_core.get_item(item_id)

        if item is None:
            return False

        driver_command = OrcDriverCmd()
        driver_command.set_type(item.item_type)
        driver_command.set_mode(item.item_mode)

        if self._key is None:
            self.__logger.error('Resource is None')

        # Web 步骤
        if driver_command.is_web():

            web_command = WebCmd()

            try:

                web_command.set_cmd(json.loads(item.item_operate))
                web_command.set_mode(driver_command.operate_mode)

                if web_command.data_num:
                    data = self._data_client.get_cmd_data(
                        OrcRecordCmd(p_item_path[-1]), web_command.cmd_object, self.__func_step)
                    if not data:
                        self.__logger.error('no enough data to run command %s' % web_command.get_cmd_dict())
                    web_command.set_data(data)

            except (TypeError, ValueError):
                return False

            driver_command.set_cmd(web_command)
            self._command.set_cmd(driver_command)

            result = self._driver_lib.resource(self._key).get(self._command.get_cmd_dict())

            if not ResourceCheck.result_status(result, u"执行命令 %s" % web_command.get_cmd_dict(), self.__logger):
                return False

            _result = result.data

            # 执行项
            if driver_command.is_operation():

                pic_name = os.path.join(self._case_folder, "%s.png" % self._data_flag)

                try:
                    self._service_core.get_web_pic(pic_name)
                except Exception:
                    self.__logger.error("Saver image error, %s" % pic_name)

            # 检查项
            elif driver_command.is_check():
                _result = web_command.data_chk == _result

            else:
                pass

        elif driver_command.is_data():

            data_command = DataCmd()

            data_command.set_cmd(json.loads(item.item_operate))
            data_command.set_data(self._service_core.get_data(self._env, p_item_path, data_command.cmd_object))

            _result = data_command.get_cmd_dict()['DATA']

            if driver_command.is_check():
                _result = _result[0] == _result[1]

        else:
            pass

        return _result

    def apply(self):
        """
        占用测试机并设置相关参数
        :return:
        """
        for _key in self._driver_lib.driver_keys:

            if self._driver_lib.status(_key).is_waiting():
                self._occupy(_key)
                return True

        return False

    def _occupy(self, p_key):
        """
        占用一个驱动
        :param p_key:
        :return:
        """
        # 生成 session
        self._sessions.create_session()

        # 占用驱动
        self._sys_command.set_occupy()
        self._command.set_session(self._sessions.session)
        self._command.set_cmd(self._sys_command)

        result = self._driver_lib.resource(p_key).get(self._command.get_cmd_dict())

        if not ResourceCheck.result_status(result, 'Error: occupy driver %s failed' % p_key):
            return False

        # 设置参数
        self._sys_command.set_parameter()
        self._sys_command.set_data(self._parameter)
        self._command.set_session(self._sessions.session)
        self._command.set_cmd(self._sys_command)

        result = self._driver_lib.resource(p_key).get(self._command.get_cmd_dict())

        if not ResourceCheck.result_status(result, 'Error: set parameter %s failed' % self._parameter):
            return False

        self._key = p_key

        return True

    def release(self):
        """
        释放驱动
        :param p_key:
        :return:
        """
        self._sys_command.set_release()
        self._command.set_cmd(self._sys_command)

        result = self._driver_lib.resource(self._key).get(self._command.get_cmd_dict())

        if not ResourceCheck.result_status(result, 'Error: release driver %s failed' % self._key):
            return False

        return True


class Recoder(object):
    """
    记录管理
    """
    def __init__(self):

        object.__init__(self)

        self._configer = get_config()
        self._home = self._configer.get_option("RUN", "home")

        # 记录目录
        self._rec_path = self._home

        # 记录文件
        self._rec_file = None

    def set_path(self, p_path):
        """
        通过路径获取到执行记录文件,需要转换目录格式进行对比
        :param p_path: {pid, id}
        :param p_path: dict
        :return:
        """
        item_pid = p_path["pid"]
        item_id = re.sub('.*:', '', p_path["id"])

        rec_path = None

        for _group in os.listdir(self._home):

            _group_id = _group.split("_")[1]

            if _group_id == item_pid:
                rec_path = os.path.join(self._home, _group)

        if rec_path is not None:
            self._rec_path = os.path.join(rec_path, item_id)
            self._rec_file = os.path.join(self._rec_path, 'default.res')

    def get_rec_file(self):
        """
        获取记录文件
        :return:
        """
        return self._rec_file

    def get_run_home(self):
        """
        获取运行CASE的目录
        :return:
        """
        return self._rec_path


class CaseAllot(RunData):
    """
    用例分配
    """
    def __init__(self):

        RunData.__init__(self)

        self._node = None

    def init(self, p_file):
        """

        :param p_file:
        :return:
        """
        self.load_data_list(p_file)

    def cases(self, p_node=None):
        """
        case 迭代器
        :param p_node:
        :return:
        """
        self._node = self.tree if p_node is None else p_node

        cmd = OrcRecordCmd(self._node['content'])
        children = self._node['children']

        if cmd.is_case():
            yield children
        else:
            for child in children:
                for _cmd in self.cases(child):
                    yield _cmd

    def get_current_path(self, p_tree=None):
        """

        :param p_tree:
        :return:
        """
        tree = p_tree or self.tree
        if not tree['content']:
            tree = tree['children'][0]

        item_path = list()

        if self._node is None:
            return item_path

        if tree == self._node:
            item_path.append(tree['content'])
            return item_path

        for _child in tree['children']:
            res = self.get_current_path(_child)
            if res:
                item_path.append(tree['content'])
                item_path.extend(res)
                return item_path

        return []


class DriverLib(object):
    """
    驱动信息库
    """
    def __init__(self):

        object.__init__(self)

        self._configer_run = get_config('run')

        # 驱动信息库
        self._driver_lib = dict()

        self.driver_keys = self._configer_run.get_option('DRIVER', 'list')
        self.driver_keys = self.driver_keys.split(',')
        for i in range(len(self.driver_keys)):
            self.driver_keys[i] = self.driver_keys[i].replace(' ', '')

        for _name in self.driver_keys:
            self._driver_lib[_name] = [
                OrcDriverStatus(_name),
                OrcDriverResource(_name)
            ]

    def status(self, p_key):
        """
        返回状态
        :param p_key:
        :return:
        :rtype: OrcDriverStatus
        """
        if p_key not in self._driver_lib:
            return None
        else:
            return self._driver_lib[p_key][0]

    def resource(self, p_key):
        """
        返回资源
        :param p_key:
        :return:
        :rtype: OrcDriverResource
        """
        if p_key not in self._driver_lib:
            return None
        else:
            return self._driver_lib[p_key][1]
