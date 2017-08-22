# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibDataStruct import ListTree
from OrcLib.LibCmd import OrcRecordCmd

from OrcLib.LibDatabase import TabBatchDet
from OrcLib.LibDatabase import TabCaseDef
from OrcLib.LibDatabase import TabCaseDet
from OrcLib.LibDatabase import TabStepDet
from OrcLib.LibType import DataScopeType


class CaseData(ListTree):
    """
    数据库查找 batch/case/step... 并生成列表及树结构
    """
    def __init__(self):

        ListTree.__init__(self)

        # Log
        self._logger = OrcLog("basic.lib_frame.case_data")

        # Source
        self._resource_batch_def = OrcResource("BatchDef")
        self._resource_batch_det = OrcResource("BatchDet")
        self._resource_case_def = OrcResource("CaseDef")
        self._resource_case_det = OrcResource("CaseDet")
        self._resource_step_def = OrcResource("StepDef")
        self._resource_step_det = OrcResource("StepDet")
        self._resource_item = OrcResource("Item")

        self._root_id = ''

        # 未经格式化的原始数据
        self._raw_data = list()

    def load_batch(self, p_id):
        """
        载入计划数据
        :param p_id:
        :return:
        """
        self.load(DataScopeType.BATCH, p_id)

    def load_case(self, p_id):
        """
        载入用例数据
        :param p_id:
        :return:
        """
        self.load(DataScopeType.CASE, p_id)

    def load_step(self, p_id):
        """
        载入步骤数据
        :param p_id:
        :return:
        """
        self.load(DataScopeType.STEP, p_id)

    def load(self, p_type, p_id):
        """
        载入数据
        :param p_type:
        :param p_id:
        :return:
        """
        if p_type not in DataScopeType.all():
            return []

        if p_type == DataScopeType.BATCH:
            self.list = self._get_batch_list(p_id)
            self.resolve_list()

        elif p_type == DataScopeType.CASE:
            self.list = self._get_case_list(p_id)
            self.resolve_list()

        elif p_type == DataScopeType.STEP:
            self.list = self._get_item_list(p_id)
            self.resolve_list()

        else:
            pass

    def get_items(self):
        """
        获取数据中的 item
        :return:
        """
        rtn = []

        for _data in self.list:
            cmd = OrcRecordCmd(_data)

            if cmd.is_item_type():
                rtn.append(self.raw_data(cmd.id))

        return rtn

    def raw_data(self, p_id):
        """
        获取取以 id 标识的原始数据
        :param p_id:
        :return:
        """
        for item in self._raw_data:
            if item['id'] == p_id:
                return item

        return None

    def _get_batch_list(self, p_id):
        """
        获取批及期所有用例数据列表
        :param p_id: batch def id
        :return:
        """
        # 返回
        rtn = list()

        # 命令,用于判断数据类型
        cmd = OrcRecordCmd()

        # 获取批数据
        batch_defs = self._resource_batch_def.get(parameter=dict(id=p_id, type="tree"))

        if not ResourceCheck.result_status(batch_defs, u"查询计划列表", self._logger):
            return list()

        self._raw_data.extend(batch_defs.data)

        # 循环获取用例
        for _batch_def_data in batch_defs.data:

            # 批执行数据
            cmd.batch(_batch_def_data)

            # 批数据加入到列表
            rtn.append(cmd.to_dict())

            # 类型为 batch 时,加入case
            if cmd.is_batch():

                # 获取 case 列表(batch_det)
                batch_dets = self._resource_batch_det.get(parameter=dict(batch_id=cmd.id))

                if not ResourceCheck.result_status(batch_dets, u"查询用例列表", self._logger):
                    return list()

                # 加入 case 及其内容
                for _batch_det_data in batch_dets.data:

                    _batch_det = TabBatchDet(_batch_det_data)
                    _case_list = self._get_case_list(_batch_det.case_id, _batch_det.batch_id)

                    rtn.extend(_case_list)

        return rtn

    def _get_case_list(self, p_id, p_pid=None, p_mode=None):
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

        self._raw_data.extend(case_defs.data)

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
                _step_list = self._get_step_list(cmd.id)
                rtn.extend(_step_list)

        return rtn

    def _get_step_list(self, p_id):
        """
        获取用例步骤及其所有子元素
        :param p_id: case_id
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

        self._raw_data.extend(case_dets.data)

        for _case_det_data in case_dets.data:

            _case_det = TabCaseDet(_case_det_data)

            _step = self._resource_step_def.get(path=_case_det.step_id)

            # 检查结果
            if not ResourceCheck.result_status(case_dets, u"查询步骤列表", self._logger):
                return list()

            self._raw_data.append(_step.data)

            cmd.step(_step.data, _case_det.step_no, _case_det.case_id)
            rtn.append(cmd.to_dict())

            if cmd.is_normal_step():
                rtn.extend(self._get_item_list(cmd.id))
            elif cmd.is_func_step():
                rtn.extend(self._get_func_list(cmd.id))
            else:
                pass

        return rtn

    def _get_func_list(self, p_id):
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

        self._raw_data.extend(step_dets.data)

        # 循环获取步骤内容
        for _func_data in step_dets.data:

            _func = TabStepDet(_func_data)

            rtn.extend(self._get_case_list(_func.item_id, _func.step_id, 'FUNC'))

        return rtn

    def _get_item_list(self, p_id):
        """
        获致操作项列表
        :param p_id: step_id
        :return:
        :rtype: list
        """
        rtn = list()
        cmd = OrcRecordCmd()

        # 检查结果
        step_dets = self._resource_step_det.get(parameter=dict(step_id=p_id))

        if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self._logger):
            return list()

        self._raw_data.extend(step_dets.data)

        for _step_det_data in step_dets.data:

            _step_det = TabStepDet(_step_det_data)

            _item = self._resource_item.get(path=_step_det.item_id)

            # 检查结果
            if not ResourceCheck.result_status(step_dets, u"查询步骤项列表", self._logger):
                return list()

            self._raw_data.append(_item.data)

            cmd.item(_item.data, _step_det.item_no, _step_det.step_id)

            if _item.data is not None:
                rtn.append(cmd.to_dict())

        return rtn
