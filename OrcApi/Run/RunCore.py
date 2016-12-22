# coding=utf-8
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from OrcLib import get_config
from OrcLib.LibState import RunState
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibDataStruct import ListTree
from RunService import RunCoreService
from RunLog import RunLog


class RunCore(ListTree):
    """
    Window service
    """

    def __init__(self):

        ListTree.__init__(self)

        # Log
        self.__logger = OrcLog("view.driver.service.window")

        # Source
        self.__resource_batch_def = OrcHttpResource("BatchDef")
        self.__resource_batch_det = OrcHttpResource("BatchDet")
        self.__resource_case_def = OrcHttpResource("CaseDef")
        self.__resource_case_det = OrcHttpResource("CaseDet")
        self.__resource_step_def = OrcHttpResource("StepDef")
        self.__resource_step_det = OrcHttpResource("StepDet")
        self.__resource_item = OrcHttpResource("Item")

        self.__service = RunCoreService()

        self.__home = get_config().get_option("RUN", "home")
        self.__home_run = None  # 运行时目录,为home目录/case(batch)/time

        self.__list = []  # 列表
        self.__root_id = None  # 根元素 id

        self.__run_list = []  # 执行列表,batch->item,用于查找数据及控件...
        self.__run_logger = RunLog()

    def get_home(self):
        return self.__home

    def search_list(self, p_type, p_id):
        """
        获取执行列表,可能是 CASE 或者 BATCH
        :param p_id:
        :param p_type:
        :return:
        """
        self.__root_id = p_id

        if "BATCH" == p_type:
            _list = self.__get_batch_list(p_id)
        else:
            _list = self.__get_case_list(p_id)

        self.resolve("LIST", _list)

    def __get_batch_list(self, p_id):
        """
        获取批及期所有用例数据列表
        :param p_id:
        :return:
        """
        rtn = list()
        batches = self.__resource_batch_def.get(dict(id=p_id, type="tree"))

        if not batches:
            return None

        for _batch in batches:

            _batch_id = _batch["id"]
            _type = _batch["batch_type"]

            rtn.append(RunData("BatchDef", _batch).__dict__)

            if "BATCH" == _type:

                cases = self.__resource_batch_det.get(dict(batch_id=_batch_id))

                for _case in cases:
                    _case_id = _case["case_id"]
                    _case_list = self.__get_case_list(_case_id, _batch_id)

                    rtn.extend(_case_list)

        return rtn

    def __get_case_list(self, p_id, p_batch_id=None):
        """
        获取用例组及其所有子元素
        :param p_id:
        :param p_batch_id:
        :return:
        :rtype: list
        """
        rtn = list()
        cases = self.__resource_case_def.get(dict(id=p_id, type="tree"))

        if not cases:
            return None

        for _case in cases:

            _id = _case["id"]
            _type = _case["case_type"]

            rtn.append(RunData("CaseDef", _case, p_batch_id).__dict__)

            if "CASE" == _type:
                _step_list = self.__get_step_list(_id)
                rtn.extend(_step_list)

        return rtn

    def __get_step_list(self, p_id):
        """
        获取步骤及其所有子元素
        :param p_id:
        :return:
        :rtype: list
        """
        rtn = list()

        case_dets = self.__resource_case_det.get(dict(case_id=p_id))

        if not case_dets:
            return []

        for _step_info in case_dets:
            _step_id = _step_info["step_id"]
            _case_id = _step_info["case_id"]

            self.__resource_step_def.set_path(_step_id)
            _step = self.__resource_step_def.get()

            rtn.append(RunData("StepDef", _step, _case_id).__dict__)
            rtn.extend(self.__get_item_list(_step_id))

        return rtn

    def __get_item_list(self, p_id):
        """
        获致操作项列表
        :param p_id:
        :return:
        :rtype: list
        """
        rtn = list()
        step_dets = self.__resource_step_det.get(dict(step_id=p_id))

        if not step_dets:
            return []

        for _item_info in step_dets:
            _item_id = _item_info["item_id"]
            _step_id = _item_info["step_id"]

            self.__resource_item.set_path(_item_id)
            _item = self.__resource_item.get()

            rtn.append(RunData("Item", _item, _step_id).__dict__)

        return rtn

    def save_list(self, p_file):
        """
        把 list 存储为xml
        :param p_file:
        :return:
        """

        def indent(p_elem, p_level=0):
            """
            格式化 xml
            :param p_level:
            :param p_elem:
            """
            _symbol = "\n" + p_level * "    "

            if len(p_elem):

                if not p_elem.text or not p_elem.text.strip():
                    p_elem.text = _symbol + "    "

                _len = len(p_elem)
                for i in xrange(_len):

                    _element = p_elem[i]
                    indent(p_elem[i], p_level + 1)

                    if not _element.tail or not _element.tail.strip():

                        if i != _len - 1:
                            _element.tail = _symbol + "    "
                        else:
                            _element.tail = _symbol

            return p_elem

        root_node = self.__list2etree()
        indent(root_node)

        xml_file = ElementTree(root_node)
        xml_file.write(p_file)

    def __list2etree(self, p_node=None):

        if p_node is None:
            _node = self.tree
        else:
            _node = p_node

        content = _node["content"]
        if content["pid"] is None:
            content["pid"] = ""

        element = Element(content["run_det_type"], content)

        for _item in _node["children"]:
            element.append(self.__list2etree(_item))

        return element

    def load_list(self, p_path):
        """
        从文件中读取数据
        :param p_path:
        :return:
        """
        if not os.path.exists(p_path):
            return None

        element = ElementTree()
        element.parse(p_path)

        _list = self.__xml2list(element.getroot())
        self.resolve("LIST", _list)

    def __xml2list(self, p_node):
        """
        :param p_node:
        :type p_node: Element
        :return:
        """
        if not p_node.attrib["pid"]:
            p_node.attrib["pid"] = None

        res = [p_node.attrib]

        for _node in p_node:
            res.extend(self.__xml2list(_node))

        return res

    def run_start(self, p_path):
        """

        :param p_path:
        :return:
        """
        item_pid = p_path["pid"]
        item_id = p_path["id"]
        item_path = None

        for _group in os.listdir(self.__home):

            _group_id = _group.split("_")[1]

            if _group_id == item_pid:
                item_path = "%s/%s" % (self.__home, _group)

        if item_path is not None:
            self.__home_run = "%s/%s" % (item_path, item_id)
            item_path = "%s/default.res" % self.__home_run

        self.load_list(item_path)
        self.run(self.tree)
        self.save_list(item_path)

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


class RunData:
    """
    用例数据类型与界面类型转换
    """
    def __init__(self, p_type, p_data, p_pid=None):

        self.id = None
        self.pid = None
        self.run_det_type = None
        self.flag = None
        self.desc = None
        self.status = "WAITING"

        self.__type = p_type

        if "BatchDef" == self.__type:

            from OrcLib.LibDatabase import TabBatchDef

            _data = TabBatchDef(p_data)

            self.id = _data.id
            self.pid = _data.pid
            self.run_det_type = "BATCH" if "BATCH" == _data.batch_type else "BATCH_GROUP"
            self.flag = _data.batch_no
            self.desc = _data.batch_desc

        elif "CaseDef" == self.__type:

            from OrcLib.LibDatabase import TabCaseDef

            _data = TabCaseDef(p_data)

            self.id = _data.id
            self.pid = _data.pid
            self.run_det_type = "CASE" if "CASE" == _data.case_type else "CASE_GROUP"
            self.flag = _data.case_no
            self.desc = _data.case_desc

        elif "StepDef" == self.__type:

            from OrcLib.LibDatabase import TabStepDef

            _data = TabStepDef(p_data)

            self.id = _data.id
            self.run_det_type = "STEP"
            self.flag = _data.id
            self.desc = _data.step_desc

        elif "Item" == self.__type:

            from OrcLib.LibDatabase import TabItem

            _data = TabItem(p_data)

            self.id = _data.id
            self.run_det_type = "ITEM"
            self.flag = _data.id
            self.desc = _data.item_desc

        if self.pid is None or "None" == self.pid:
            self.pid = p_pid
