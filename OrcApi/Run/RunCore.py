# coding=utf-8
import os
import re
import threading

from OrcLib import get_config
from OrcLib.LibLog import OrcLog

from RunService import RunCoreService
from OrcLib.LibRunTime import OrcRunStatus
from RunData import RunData
from RunLog import RunLog
from RunData import RunCmdType


class RunCore(object):

    def __init__(self):

        object.__init__(self)

        self.__launch = RunLaunch()
        self.__status = OrcRunStatus()
        self.thread = None

    def start(self, p_path):
        """
        执行
        :param p_path:
        :return:
        """
        if self.__status.status:
            return False, u'驱动忙'

        self.__status.director = True

        self.thread = threading.Thread(target=self.__launch.run_start, args=(p_path,))
        self.thread.setDaemon(True)
        self.thread.start()

        return True, u'开始执行'

    def stop(self):
        """
        终止
        :return:
        """
        self.__status.director = False

    def get_status(self):
        """
        获取状态
        :return:
        """
        return self.__status.status


class RunLaunch(RunData):
    """
    Window service
    """
    def __init__(self):

        RunData.__init__(self)

        # Log 普通日志
        self.__logger = OrcLog("resource.run.run_core")

        # 执行记录
        self.__run_logger = RunLog()

        self.__service_core = RunCoreService()
        self.__service_status = OrcRunStatus()

        self.__home = get_config().get_option("RUN", "home")
        self.__home_run = None  # 运行时目录,为home目录/case(batch)/time

        self.__list = []  # 列表

        # 执行列表,batch->item,用于查找数据及控件...
        self.__run_list = []

    def run_start(self, p_path):
        """
        读取运行记录文件并逐条执行
        :param p_path:
        :return:
        """
        # 运行测试
        item_pid = p_path["pid"]
        item_id = re.sub('.*:', '', p_path["id"])
        item_path = None

        # 清空状态数据
        self.__service_status.clean()
        self.__service_status.director = True
        self.__service_status.status = True

        for _group in os.listdir(self.__home):

            _group_id = _group.split("_")[1]

            if _group_id == item_pid:
                item_path = os.path.join(self.__home, _group)

        if item_path is not None:
            self.__home_run = os.path.join(item_path, item_id)
            item_path = os.path.join(self.__home_run, 'default.res')

        self.load_list(item_path)

        self.run(self.tree)

        self.__service_status.director = False
        self.__service_status.status = False

        self.update_list(item_path)

    def run(self, p_node):
        """
        :param p_node:
        :return:
        """
        # 终止
        if not self.__service_status.director:
            self.__service_status.status = False
            return False

        # 设置默认状态
        self.__service_status.status = True

        result = True

        cmd = RunCmdType(p_node['content'])
        children = p_node['children']

        self.__run_list.append(p_node["content"])

        self.__run_logger.set_list(self.__home_run, self.__run_list)
        self.__run_logger.run_begin()

        # 如果是 item 运行步骤
        if cmd.is_item_type():
            result = self.__run_step(self.__run_list)

        # 不是 item,运行子节点
        else:
            if not children:
                result = None

            else:
                for _sub_step in children:

                    _result = self.run(_sub_step)

                    # 更新状态
                    if result is None:
                        result = None

                    elif _result is None:
                        result = None

                    else:
                        result = result and _result

                    # 如果有一个步骤没有通过,忽略剩余的步骤
                    if cmd.is_step_type() and not _result:
                        break

        # 转换状态
        if result is None:
            cmd.status.reset()
        elif result:
            cmd.status.set_pass()
        else:
            cmd.status.set_fail()

        self.__run_logger.set_list(self.__home_run, self.__run_list)
        self.__run_logger.run_end(cmd.status)

        self.__run_list.pop()

        # 更新文件状态
        p_node["content"]["status"] = cmd.status.get_status()

        # 设置进度 + 1, 并写入执行信息
        self.__service_status.step_message(cmd.to_dict())

        return result

    def __run_step(self, p_node_list):
        """
        {'status': 'WAITING',
         'flag': '20161028153349',
         'run_det_type': 'BATCH_SUIT',
         'pid': None, 'id': '1000000001',
         'desc': 'BATCH_001'}
        :param p_node_list:
        :return:
        """
        import json

        _result = None

        # 执行该 list 的最后一项,最后一项为 item, 其他为路径用于数据查找
        item_id = p_node_list[len(p_node_list) - 1]["id"]
        item = self.__service_core.get_item(item_id)

        if item is None:
            return False

        item_operation = json.loads(item.item_operate)

        # 步骤需要数据时读取数据
        if "DATA" in item_operation:

            data = self.__service_core.get_data(self.__run_list, item_operation["OBJECT"])

            if data:
                item_operation["DATA"] = data
            else:
                self.__run_logger.data("Run message: %s data is not found" % item_operation)
                return False

        # Web 步骤
        if "WEB" == item.item_type:

            # 执行项
            if "OPERATE" == item.item_mode:
                _result = self.__service_core.launch_web_step(item_operation)
                folder = self.__run_logger.get_folder()
                pic_name = os.path.join(folder, "%s.png" % item_id)
                self.__service_core.get_web_pic(pic_name)

            # 检查项
            elif "CHECK" == item.item_mode:
                _result = self.__service_core.check_web_step(item_operation)

            else:
                pass

        self.__run_logger.data("Run message: %s" % item_operation)

        return _result
