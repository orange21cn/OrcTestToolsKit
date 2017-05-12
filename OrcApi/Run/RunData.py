# coding=utf-8
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import ParseError
from xml.etree.ElementTree import Element

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibProgram import OrcFactory
from OrcLib.LibState import RunStatus
from OrcLib.LibDataStruct import ListTree
from OrcLib.LibDatabase import TabBatchDef
from OrcLib.LibDatabase import TabBatchDet
from OrcLib.LibDatabase import TabCaseDef
from OrcLib.LibDatabase import TabCaseDet
from OrcLib.LibDatabase import TabStepDef
from OrcLib.LibDatabase import TabStepDet
from OrcLib.LibDatabase import TabItem


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

        self.__root_id = ''

    def search_list(self, p_type, p_id):
        """
        获取执行列表,可能是 CASE 或者 BATCH
        :param p_id:
        :param p_type:
        :return:
        """
        self.__root_id = p_id

        # 查找计划数据
        if "BATCH" == p_type:
            _list = self.get_batch_list(p_id)

        # 查找用例数据
        else:
            _list = self.get_case_list(p_id)

        self.resolve("LIST", _list)

    def get_batch_list(self, p_id):
        """
        获取批及期所有用例数据列表
        :param p_id:
        :return:
        """
        # 返回
        rtn = list()

        # 命令,用于将数据库数据转换为执行的命令
        cmd = RunCmdType()

        # 获取批数据
        batch_defs = self.__resource_batch_def.get(parameter=dict(id=p_id, type="tree"))

        if not ResourceCheck.result_status(batch_defs, u"查询计划列表", self.__logger):
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
                batch_dets = self.__resource_batch_det.get(parameter=dict(batch_id=_batch_def.id))

                if not ResourceCheck.result_status(batch_dets, u"查询用例列表", self.__logger):
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
        cmd = RunCmdType()

        # 模式,CASE 时不查找 FUNC 数据, STEP 时查找步骤
        mode = 'CASE' if p_mode is None else p_mode

        # 用例列表
        case_defs = self.__resource_case_def.get(parameter=dict(id=p_id, type="tree"))

        if not ResourceCheck.result_status(case_defs, u"查询用例列表", self.__logger):
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
                _step_list = self.__get_step_list(cmd.id)
                rtn.extend(_step_list)

        return rtn

    def __get_step_list(self, p_id):
        """
        获取步骤及其所有子元素
        :param p_id:
        :return:
        :rtype: list
        """
        # 返回
        rtn = list()

        # 命令,用于将数据库数据转换为执行的命令
        cmd = RunCmdType()

        # 获取用例步骤数据
        case_dets = self.__resource_case_det.get(parameter=dict(case_id=p_id))

        if not ResourceCheck.result_status(case_dets, u"查询用例步骤列表", self.__logger):
            return list()

        for _case_det_data in case_dets.data:

            _case_det = TabCaseDet(_case_det_data)

            _step = self.__resource_step_def.get(path=_case_det.step_id)

            # 检查结果
            if not ResourceCheck.result_status(case_dets, u"查询步骤列表", self.__logger):
                return list()

            cmd.step(_step.data, _case_det.step_no, _case_det.case_id)
            rtn.append(cmd.to_dict())

            if cmd.is_normal_step():
                rtn.extend(self.__get_item_list(cmd.id))
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
        step_dets = self.__resource_step_det.get(parameter=dict(step_id=p_id))

        if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self.__logger):
            return list()

        # 循环获取步骤内容
        for _func_data in step_dets.data:

            _func = TabStepDet(_func_data)

            rtn.extend(self.get_case_list(_func.item_id, _func.step_id, 'FUNC'))

        return rtn

    def __get_item_list(self, p_id):
        """
        获致操作项列表
        :param p_id:
        :return:
        :rtype: list
        """
        rtn = list()
        cmd = RunCmdType()

        # 检查结果
        step_dets = self.__resource_step_det.get(parameter=dict(step_id=p_id))

        if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self.__logger):
            return list()

        for _step_det_data in step_dets.data:

            _step_det = TabStepDet(_step_det_data)

            _item = self.__resource_item.get(path=_step_det.item_id)

            # 检查结果
            if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self.__logger):
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
        self.search_list(p_type, p_id)
        self.update_list(p_file)

    def update_list(self, p_file):
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
        try:
            element.parse(p_path)
        except ParseError:
            return

        # 获取数据
        _list = self.__xml2list(element.getroot())

        # 解析成 tree
        self.resolve("LIST", _list)

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


class RunCmdType(object):
    """
    测试条目类型
    """
    class Status(object):
        """
        执行状态, new -> waiting -> running -> pass/fail
        """
        def __init__(self, p_status=None):

            object.__init__(self)

            if p_status is None:
                self._status = RunStatus.new_
            else:
                self._status = p_status

        def reset(self):
            """
            重置为 new
            :return:
            """
            self._status = RunStatus.new_

        def set_waiting(self):
            """
            设置为 waiting 状态
            :return:
            """
            self._status = RunStatus.waiting_

        def set_running(self):
            """
            设置为 running 状态
            :return:
            """
            self._status = RunStatus.running_

        def set_pass(self):
            """
            设置为通过
            :return:
            """
            self._status = RunStatus.pass_

        def set_fail(self):
            """
            设置为 fail
            :return:
            """
            self._status = RunStatus.fail_

        def is_new(self):
            """
            new
            :return:
            """
            return RunStatus.new_ == self._status

        def is_waiting(self):
            """
            waiting status
            :return:
            """
            return RunStatus.waiting_ == self._status

        def is_running(self):
            """
            running status
            :return:
            """
            return RunStatus.running_ == self._status

        def is_pass(self):
            """
            pass status
            :return:
            """
            return RunStatus.pass_ == self._status

        def is_fail(self):
            """
            fail status
            :return:
            """
            return RunStatus.fail_ == self._status

        def get_status(self):
            """
            获取状态
            :return:
            """
            return self._status

    def __init__(self, p_cmd=None):
        """
        init, cmd str to type
        :param p_cmd:
        :return:
        """
        object.__init__(self)

        inp = OrcFactory.create_dict(p_cmd)

        # id
        self.id = inp.value('id')

        # parent id
        self.pid = inp.value('pid')

        # type
        self.run_det_type = inp.value('run_det_type')

        # flag
        self.flag = inp.value('flag')

        # description
        self.desc = inp.value('desc')

        # status
        self.status = self.Status(inp.value('status'))

    def batch(self, p_data):
        """
        batch init func, database data to type
        :param p_data:
        :return:
        """
        _data = TabBatchDef(p_data)

        self.id = _data.id
        self.pid = _data.pid
        self.run_det_type = _data.batch_type
        self.flag = _data.batch_no
        self.desc = _data.batch_desc

    def case(self, p_data, p_pid=None):
        """
        case init func, database data to type
        :param p_pid:
        :param p_data:
        :return:
        """
        _data = TabCaseDef(p_data)

        self.id = _data.id
        self.pid = _data.pid
        self.run_det_type = _data.case_type
        self.flag = _data.case_no
        self.desc = _data.case_desc

        if p_pid is not None:
            self.pid = p_pid

    def step(self, p_data, p_no, p_pid=None):
        """
        step init func, database data to type
        :param p_no:
        :param p_pid:
        :param p_data:
        :return:
        """
        _data = TabStepDef(p_data)

        self.id = _data.id
        self.run_det_type = _data.step_type
        self.flag = p_no
        self.desc = _data.step_desc

        if p_pid is not None:
            self.pid = p_pid

    def item(self, p_data, p_no, p_pid=None):
        """
        item init func database data to type
        :param p_pid:
        :param p_no:
        :param p_data:
        :return:
        """
        _data = TabItem(p_data)

        self.id = _data.id
        self.run_det_type = _data.item_type
        self.flag = p_no
        self.desc = _data.item_desc

        if p_pid is not None:
            self.pid = p_pid

    def is_batch_type(self):
        """
        batch type, include batch and batch suit
        :return:
        """
        return self.run_det_type in ('BATCH_SUITE', 'BATCH')

    def is_batch_suite(self):
        """
        batch suite
        :return:
        """
        return self.run_det_type == 'BATCH_SUITE'

    def is_batch(self):
        """
        batch
        :return:
        """
        return self.run_det_type == 'BATCH'

    def is_case_type(self):
        """
        case type, include case and case suite
        :return:
        """
        return self.run_det_type in ('CASE_SUITE', 'CASE', 'FUNC_SUITE', 'FUNC')

    def is_cases(self):
        """
        case suit, case
        :return:
        """
        return self.run_det_type in ('CASE_SUITE', 'CASE')

    def is_funcs(self):
        """
        function suit, function
        :return:
        """
        return self.run_det_type in ('FUNC_SUITE', 'FUNC')

    def is_case_suite(self):
        """
        case suite
        :return:
        """
        return self.run_det_type == 'CASE_SUITE'

    def is_case(self):
        """
        case
        :return:
        """
        return self.run_det_type == 'CASE'

    def is_func_suite(self):
        """
        function suite
        :return:
        """
        return self.run_det_type == 'FUNC_SUITE'

    def is_func(self):
        """
        function
        :return:
        """
        return self.run_det_type == 'FUNC'

    def is_step_type(self):
        """
        normal step and function step
        :return:
        """
        return self.run_det_type in ('STEP_NORMAL', 'STEP_FUNC')

    def is_normal_step(self):
        """
        normal step
        :return:
        """
        return self.run_det_type == 'STEP_NORMAL'

    def is_func_step(self):
        """
        function step
        :return:
        """
        return self.run_det_type == 'STEP_FUNC'

    def is_item_type(self):
        """
        item type, include ....
        :return:
        """
        return self.run_det_type in ('WEB',)

    def is_web_item(self):
        """
        web item
        :return:
        """
        return self.run_det_type == 'WEB'

    def to_dict(self):
        """
        转换为 json/dict
        :return:
        """
        return dict(
            id=self.id,
            pid=self.pid,
            run_det_type=self.run_det_type,
            flag=self.flag,
            desc=self.desc,
            status=self.status.get_status()
        )
