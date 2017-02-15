# coding=utf-8
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibDataStruct import ListTree
from OrcLib.LibNet import ResourceCheck


class RunData(ListTree):
    """

    """
    def __init__(self):

        ListTree.__init__(self)

        # Log
        self.__logger = OrcLog("resource.run.run_data")

        # Source
        self.__resource_batch_def = OrcResource("BatchDef")
        self.__resource_batch_det = OrcResource("BatchDet")
        self.__resource_case_def = OrcResource("CaseDef")
        self.__resource_case_det = OrcResource("CaseDet")
        self.__resource_step_def = OrcResource("StepDef")
        self.__resource_step_det = OrcResource("StepDet")
        self.__resource_item = OrcResource("Item")

    def search_list(self, p_type, p_id):
        """
        获取执行列表,可能是 CASE 或者 BATCH
        :param p_id:
        :param p_type:
        :return:
        """
        self.__root_id = p_id

        if "BATCH" == p_type:
            # _list = self.__get_batch_list(p_id)
            _list = self.get_batch_list(p_id)
        else:
            # _list = self.__get_case_list(p_id)
            _list = self.get_case_list(p_id)

        self.resolve("LIST", _list)

    def get_batch_list(self, p_id):
        """
        获取批及期所有用例数据列表
        :param p_id:
        :return:
        """
        rtn = list()
        batches = self.__resource_batch_def.get(parameter=dict(id=p_id, type="tree"))

        # 检查结果
        if not ResourceCheck.result_status(batches, u"查询计划列表", self.__logger):
            return list()

        for _batch in batches.data:

            _batch_id = _batch["id"]
            _type = _batch["batch_type"]

            rtn.append(RunType("BatchDef", _batch).__dict__)

            if "BATCH" == _type:

                cases = self.__resource_batch_det.get(parameter=dict(batch_id=_batch_id))

                # 检查结果
                if not ResourceCheck.result_status(cases, u"查询用例列表", self.__logger):
                    return list()

                for _case in cases.data:
                    _case_id = _case["case_id"]
                    _case_list = self.get_case_list(_case_id, _batch_id)

                    rtn.extend(_case_list)

        return rtn

    def get_case_list(self, p_id, p_batch_id=None):
        """
        获取用例组及其所有子元素
        :param p_id:
        :param p_batch_id:
        :return:
        :rtype: list
        """
        rtn = list()
        cases = self.__resource_case_def.get(parameter=dict(id=p_id, type="tree"))

        # 检查结果
        if not ResourceCheck.result_status(cases, u"查询用例列表", self.__logger):
            return list()

        for _case in cases.data:

            _id = _case["id"]
            _type = _case["case_type"]

            if _id == p_id:
                _case['pid'] = p_batch_id

            rtn.append(RunType("CaseDef", _case, p_batch_id).__dict__)

            if _type in ("CASE", "FUNC"):
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

        case_dets = self.__resource_case_det.get(parameter=dict(case_id=p_id))

        # 检查结果
        if not ResourceCheck.result_status(case_dets, u"查询用例步骤列表", self.__logger):
            return list()

        for _step_info in case_dets.data:
            _step_id = _step_info["step_id"]
            _case_id = _step_info["case_id"]

            _step = self.__resource_step_def.get(path=_step_id)

            # 检查结果
            if not ResourceCheck.result_status(case_dets, u"查询步骤列表", self.__logger):
                return list()

            rtn.append(RunType("StepDef", _step.data, _case_id).__dict__)

            _step_type = _step.data["step_type"]

            if "NORMAL" == _step_type:
                rtn.extend(self.__get_item_list(_step_id))
            elif "FUNC" == _step_type:
                rtn.extend(self.__get_func_list(_step_id))
            else:
                pass

        return rtn

    def __get_func_list(self, p_id):
        """
        获取函数列表
        :param p_id:
        :return:
        """
        rtn = list()

        step_dets = self.__resource_step_det.get(parameter=dict(step_id=p_id))

        # 检查结果
        if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self.__logger):
            return list()

        for _func_info in step_dets.data:

            _func_id = _func_info["item_id"]
            _step_id = _func_info["step_id"]

            rtn.extend(self.get_case_list(_func_id, _step_id))

        return rtn

    def __get_item_list(self, p_id):
        """
        获致操作项列表
        :param p_id:
        :return:
        :rtype: list
        """
        rtn = list()
        step_dets = self.__resource_step_det.get(parameter=dict(step_id=p_id))

        # 检查结果
        if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self.__logger):
            return list()

        for _item_info in step_dets.data:
            _item_id = _item_info["item_id"]
            _step_id = _item_info["step_id"]

            _item = self.__resource_item.get(path=_item_id)

            # 检查结果
            if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self.__logger):
                return list()

            if _item.data is not None:
                rtn.append(RunType("Item", _item.data, _step_id).__dict__)

        return rtn

    def save_list(self, p_type, p_id, p_file):
        """
        把 list 存储为xml
        :param p_id:
        :param p_type:
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

        self.search_list(p_type, p_id)

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


class RunType(object):
    """
    用例数据类型与界面类型转换
    """
    def __init__(self, p_type, p_data, p_pid=None):

        object.__init__(self)

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
            self.run_det_type = "CASE_GROUP" if "GROUP" == _data.case_type else _data.case_type
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

        else:
            pass

        if self.pid is None or "None" == self.pid:
            self.pid = p_pid
