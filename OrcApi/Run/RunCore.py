# coding=utf-8
import os

from OrcLib import get_config
from OrcLib.LibState import RunState
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from RunService import RunCoreService
from RunData import RunData
from RunLog import RunLog


class RunCore(RunData):
    """
    Window service
    """
    def __init__(self):

        RunData.__init__(self)

        # Log
        self.__logger = OrcLog("resource.run.run_core")

        # Source
        self.__resource_batch_def = OrcResource("BatchDef")
        self.__resource_batch_det = OrcResource("BatchDet")
        self.__resource_case_def = OrcResource("CaseDef")
        self.__resource_case_det = OrcResource("CaseDet")
        self.__resource_step_def = OrcResource("StepDef")
        self.__resource_step_det = OrcResource("StepDet")
        self.__resource_item = OrcResource("Item")

        self.__service = RunCoreService()

        self.__home = get_config().get_option("RUN", "home")
        self.__home_run = None  # 运行时目录,为home目录/case(batch)/time

        self.__list = []  # 列表

        self.__run_list = []  # 执行列表,batch->item,用于查找数据及控件...
        self.__run_logger = RunLog()

    def run_start(self, p_path):
        """

        :param p_path:
        :return:
        """
        item_pid = p_path["pid"]
        item_id = p_path["id"]
        item_path = None

        client_ip = p_path["ip"]
        client_port = p_path["port"]

        client_config = get_config("client")
        client_config.set_option("VIEW", "ip", client_ip)
        client_config.set_option("VIEW", "port", client_port)

        for _group in os.listdir(self.__home):

            _group_id = _group.split("_")[1]

            if _group_id == item_pid:
                item_path = "%s/%s" % (self.__home, _group)

        if item_path is not None:
            self.__home_run = "%s/%s" % (item_path, item_id)
            item_path = "%s/default.res" % self.__home_run

        self.load_list(item_path)
        self.run(self.tree)
        # self.save_list(item_path)

    def run(self, p_node):
        """
        :param p_node:
        :return:
        """
        result = True
        step_type = p_node["content"]["run_det_type"]

        self.__run_list.append(p_node["content"])

        self.__run_logger.set_list(self.__home_run, self.__run_list)
        self.__run_logger.run_begin()

        # 如果是 item 运行步骤
        if "ITEM" == step_type:
            result = self.__run_step(self.__run_list)

        # 不是 item,运行子节点
        else:
            if not p_node["children"]:
                result = None

            for _sub_step in p_node["children"]:

                _result = self.run(_sub_step)

                # 如果有一个步骤没有通过,忽略剩余的步骤
                if "STEP" == step_type and not _result:
                    break

                # 更新状态
                if result is None:
                    result = None

                elif _result is None:
                    result = None

                else:
                    result = result and _result

        # 转换状态
        if result is None:
            status = RunState.state_not_run
        elif result:
            status = RunState.state_pass
        else:
            status = RunState.state_fail

        self.__run_logger.set_list(self.__home_run, self.__run_list)
        self.__run_logger.run_end(status)

        self.__run_list.pop()

        # 更新文件状态
        p_node["content"]["status"] = status

        # 更新界面
        self.__service.update_status(p_node["content"])

        return result

    def __run_step(self, p_node_list):
        """
        {'status': 'WAITING',
         'flag': '20161028153349',
         'run_det_type': 'BATCH_GROUP',
         'pid': None, 'id': '1000000001',
         'desc': 'BATCH_001'}
        :param p_node_list:
        :return:
        """
        import json

        _result = None

        # 执行该 list 的最后一项,最后一项为 item, 其他为路径用于数据查找
        item_id = p_node_list[len(p_node_list) - 1]["id"]
        item = self.__service.get_item(item_id)

        if item is None:
            return False

        item_operation = json.loads(item.item_operate)

        # 步骤需要数据时读取数据
        if "DATA" in item_operation:
            data = self.__service.get_data(self.__run_list, item_operation["OBJECT"])

            if data:
                item_operation["DATA"] = data
            else:
                self.__run_logger.data("Run message: %s data is not found" % item_operation)
                return False

        # Web 步骤
        if "WEB" == item.item_type:

            # 执行项
            if "OPERATE" == item.item_mode:
                _result = self.__service.launch_web_step(item_operation)
                folder = self.__run_logger.get_folder()
                pic_name = "%s/%s.png" % (folder, item_id)
                self.__service.get_web_pic(pic_name)

            # 检查项
            elif "CHECK" == item.item_mode:
                _result = self.__service.check_web_step(item_operation)

            else:
                pass

        self.__run_logger.data("Run message: %s" % item_operation)

        return _result
