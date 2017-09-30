# coding=utf-8
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import ParseError
from xml.etree.ElementTree import Element

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibDataStruct import ListTree
from OrcLib.LibCmd import OrcRecordCmd
from OrcLib.LibStatus import RecordStatus
from OrcLib.LibDatabase import TabBatchDef
from OrcLib.LibDatabase import TabBatchDet
from OrcLib.LibDatabase import TabCaseDef
from OrcLib.LibDatabase import TabCaseDet
from OrcLib.LibDatabase import TabStepDet


class RunData(ListTree):
    """

    """
    def __init__(self):

        ListTree.__init__(self)

        # Log
        self._logger = OrcLog("resource.run.run_data")

        # Source
        self._resource_batch_def = OrcResource("BatchDef")
        self._resource_batch_det = OrcResource("BatchDet")
        self._resource_case_def = OrcResource("CaseDef")
        self._resource_case_det = OrcResource("CaseDet")
        self._resource_step_def = OrcResource("StepDef")
        self._resource_step_det = OrcResource("StepDet")
        self._resource_item = OrcResource("Item")

        self._root_id = ''

        self._file = None

    def search_list(self, p_type, p_id):
        """
        获取执行列表,可能是 CASE 或者 BATCH
        :param p_id:
        :param p_type:
        :return:
        """
        self._root_id = p_id

        # 查找计划数据
        if "BATCH" == p_type:
            _list = self.get_batch_list(p_id)

        # 查找用例数据
        else:
            _list = self.get_case_list(p_id)

        self.load("LIST", _list)

    def get_batch_list(self, p_id):
        """
        获取批及期所有用例数据列表
        :param p_id:
        :return:
        """
        # 返回
        rtn = list()

        # 命令,用于将数据库数据转换为执行的命令
        cmd = OrcRecordCmd()

        # 获取批数据
        batch_defs = self._resource_batch_def.get(parameter=dict(id=p_id, type="tree"))

        if not ResourceCheck.result_status(batch_defs, u"查询计划列表", self._logger):
            return list()

        # 循环获取用例
        for _batch_def_data in batch_defs.data:

            # 批数据类
            _batch_def = TabBatchDef(_batch_def_data)

            # 批执行数据
            cmd.batch(_batch_def_data)

            # 批数据加入到列表
            rtn.append(cmd.to_dict())

            # 类型为 batch 时,加入case
            if cmd.is_batch():

                # 获取 case 列表(batch_det)
                batch_dets = self._resource_batch_det.get(parameter=dict(batch_id=_batch_def.id))

                if not ResourceCheck.result_status(batch_dets, u"查询用例列表", self._logger):
                    return list()

                # 加入 case 及其内容
                for _batch_det_data in batch_dets.data:

                    _batch_det = TabBatchDet(_batch_det_data)
                    _case_list = self.get_case_list(_batch_det.case_id, _batch_det.batch_id)

                    rtn.extend(_case_list)

        return rtn

    def get_case_list(self, p_id, p_pid=None, p_mode=None):
        """
        获取用例组及其所有子元素
        :param p_mode:
        :param p_id:
        :param p_pid:
        :return:
        :rtype: list
        """
        # 返回
        rtn = list()

        # 命令,用于将数据库数据转换为执行的命令
        cmd = OrcRecordCmd()

        # 模式,CASE 时不查找 FUNC 数据, STEP 时查找步骤
        mode = 'CASE' if p_mode is None else p_mode

        # 用例列表
        case_defs = self._resource_case_def.get(parameter=dict(id=p_id, type="tree"))

        if not ResourceCheck.result_status(case_defs, u"查询用例列表", self._logger):
            return list()

        # 循环获取子用例及步骤
        for _case_def_data in case_defs.data:

            # 用例数据
            _case_def = TabCaseDef(_case_def_data)

            # 根节点的id为输入id,此时pid应为输入pid,忽略数据原有 pid
            if _case_def.id == p_id:
                _case_def_data['pid'] = p_pid

            # 用例命令数据
            cmd.case(_case_def_data, p_pid)

            # 普通情况下忽略 func
            if ('FUNC' == mode) or (not cmd.is_funcs()):
                rtn.append(cmd.to_dict())

            # 加入 step
            if cmd.is_case() or cmd.is_func():
                _step_list = self.get_step_list(cmd.id)
                rtn.extend(_step_list)

        return rtn

    def get_step_list(self, p_id):
        """
        获取步骤及其所有子元素
        :param p_id:
        :return:
        :rtype: list
        """
        # 返回
        rtn = list()

        # 命令,用于将数据库数据转换为执行的命令
        cmd = OrcRecordCmd()

        # 获取用例步骤数据
        case_dets = self._resource_case_det.get(parameter=dict(case_id=p_id))

        if not ResourceCheck.result_status(case_dets, u"查询用例步骤列表", self._logger):
            return list()

        for _case_det_data in case_dets.data:

            _case_det = TabCaseDet(_case_det_data)

            _step = self._resource_step_def.get(path=_case_det.step_id)

            # 检查结果
            if not ResourceCheck.result_status(case_dets, u"查询步骤列表", self._logger):
                return list()

            cmd.step(_step.data, _case_det.step_no, _case_det.case_id)
            rtn.append(cmd.to_dict())

            if cmd.is_normal_step():
                rtn.extend(self.get_item_list(cmd.id))
            elif cmd.is_func_step():
                rtn.extend(self.__get_func_list(cmd.id))
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

        # 获取步骤数据
        step_dets = self._resource_step_det.get(parameter=dict(step_id=p_id))

        if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self._logger):
            return list()

        # 循环获取步骤内容
        for _func_data in step_dets.data:

            _func = TabStepDet(_func_data)

            rtn.extend(self.get_case_list(_func.item_id, _func.step_id, 'FUNC'))

        return rtn

    def get_item_list(self, p_id):
        """
        获致操作项列表
        :param p_id:
        :return:
        :rtype: list
        """
        rtn = list()
        cmd = OrcRecordCmd()

        # 检查结果
        step_dets = self._resource_step_det.get(parameter=dict(step_id=p_id))

        if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self._logger):
            return list()

        for _step_det_data in step_dets.data:

            _step_det = TabStepDet(_step_det_data)

            _item = self._resource_item.get(path=_step_det.item_id)

            # 检查结果
            if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self._logger):
                return list()

            cmd.item(_item.data, _step_det.item_no, _step_det.step_id)

            if _item.data is not None:
                rtn.append(cmd.to_dict())

        return rtn

    def save_list(self, p_type, p_id, p_file):
        """
        把 list 存储为xml
        :param p_id:
        :param p_type:
        :param p_file:
        :return:
        """
        self._file = p_file
        self.search_list(p_type, p_id)
        self.update_list(p_file)

    def update_list(self, p_file=None):
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

        if p_file is not None:
            xml_file.write(p_file)
        else:
            xml_file.write(self._file)

    def __list2etree(self, p_node=None):

        if p_node is None:
            _node = self.tree
        else:
            _node = p_node

        if not _node['content']:
            _node = _node['children'][0]

        # Todo 如果 _node 格式不正确,报错,原因可能是没有进行查询
        content = _node["content"]

        for _key, _value in content.items():
            if _value is None:
                content[_key] = ''
            elif isinstance(_value, int):
                content[_key] = str(_value)
            else:
                pass
        if content["pid"] is None:
            content["pid"] = ""

        element = Element(content["run_det_type"], content)

        for _item in _node["children"]:
            element.append(self.__list2etree(_item))

        return element

    def load_data_list(self, p_path):
        """
        从文件中读取数据
        :param p_path:
        :return:
        """
        if not os.path.exists(p_path):
            return None
        self._file = p_path

        element = ElementTree()
        try:
            element.parse(p_path)
        except ParseError:
            return

        # 获取数据
        _list = self.__xml2list(element.getroot())

        # 解析成 tree
        self.load_list(_list)

        # 去重
        self._clean_duplication()

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

    def update_status(self, p_cmd):
        """

        :param p_cmd:
        :return:
        """
        self.update_tree(p_cmd)
        self.update_list()

    def update_tree(self, p_cmd, p_node=None):
        """
        更新状态
        :param p_cmd:
        :type p_cmd: OrcRecordCmd
        :param p_node:
        :return:
        """
        current_node = p_node or self.tree

        if not current_node['content']:
            current_node = current_node['children'][0]

        if not current_node:
            return

        current_content = current_node['content']
        current_children = current_node['children']
        current_status = RecordStatus(current_node['content']['status'])

        len_child = len(current_children)

        # 当前节点是要更新的节点
        if (current_content['run_det_type'] == p_cmd.run_det_type) and (current_content['id'] == p_cmd.id):
            current_content['status'] = p_cmd.status.status
            return p_cmd.status

        # 不是当前节点,根据子节点状态更新
        for _index in range(len_child):

            _child = current_node['children'][_index]
            _result = self.update_tree(p_cmd, _child)

            if _result is None:
                continue

            # 子节点为pass状态,非最后一节点时,不更新父节点状态
            if (len_child - 1 == _index and _result.is_pass()) or not _result.is_pass():

                current_status.plus(_result)
                current_node['content']['status'] = current_status.status
                return current_status

        return None
