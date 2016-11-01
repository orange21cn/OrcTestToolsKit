# coding=utf-8
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from OrcLib import get_config
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcInvoke
from OrcLib.LibDataStruct import ListTree


class RunCore(ListTree):
    """
    Window service
    """
    def __init__(self):

        ListTree.__init__(self)

        # Log
        self.__logger = OrcLog("view.driver.service.window")
        self.__invoker = OrcInvoke()

        # Get url from configuration
        _url = get_config("interface").get_option("DRIVER", "url")
        self.__url_list = lambda _mod: "%s/api/1.0/%s" % (_url, _mod)
        self.__url = lambda _mod, _id: "%s/%s" % (self.__url_list(_mod), _id)

        self.__home = get_config().get_option("RUN", "home")

        self.__list = []  # 列表
        self.__root_id = None  # 根元素 id

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
        url = self.__url_list("BatchDef")
        cond = dict(id=p_id, type="tree")
        batches = self.__invoker.get(url, cond)

        if not batches:
            return None

        for _batch in batches:

            _batch_id = _batch["id"]
            _type = _batch["batch_type"]

            rtn.append(RunData("BatchDef", _batch).__dict__)

            if "BATCH" == _type:

                url_det = self.__url_list("BatchDet")
                cond_det = dict(batch_id=_batch_id)
                cases = self.__invoker.get(url_det, cond_det)

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
        url = self.__url_list("CaseDef")
        cond = dict(id=p_id, type="tree")
        cases = self.__invoker.get(url, cond)

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

        url_case_det = self.__url_list("CaseDet")
        cond_case_det = dict(case_id=p_id)

        case_dets = self.__invoker.get(url_case_det, cond_case_det)

        if not case_dets:
            return []

        for _step_info in case_dets:
            _step_id = _step_info["step_id"]
            _case_id = _step_info["case_id"]
            _url_step_def = self.__url("StepDef", _step_id)

            _step = self.__invoker.get(_url_step_def)

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

        url_step_det = self.__url_list("StepDet")
        cond_step_det = dict(step_id=p_id)

        step_dets = self.__invoker.get(url_step_det, cond_step_det)

        if not step_dets:
            return []

        for _item_info in step_dets:
            _item_id = _item_info["item_id"]
            _step_id = _item_info["step_id"]

            _url_item = self.__url("Item", _item_id)
            _item = self.__invoker.get(_url_item)

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
                    indent(p_elem[i], p_level+1)

                    if not _element.tail or not _element.tail.strip():

                        if i != _len-1:
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

        self.load_list("%s/%s" % (self.__home, p_path))

        for step in self.steps():
            print step

    def run_get_status(self):

        return "OK"


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
            self.flag = _data.step_no
            self.desc = _data.step_desc

        elif "Item" == self.__type:

            from OrcLib.LibDatabase import TabItem

            _data = TabItem(p_data)

            self.id = _data.id
            self.run_det_type = "ITEM"
            self.flag = _data.item_no
            self.desc = _data.item_desc

        if self.pid is None or "None" == self.pid:
            self.pid = p_pid
