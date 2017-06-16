# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck


class FieldDefinition(object):
    """
    字段定义
    """
    def __init__(self, p_field_def):

        # 字段 id
        self.id = None if 'ID' not in p_field_def else p_field_def["ID"]

        # 字段名称
        self.name = None if 'NAME' not in p_field_def else p_field_def["NAME"]

        # 字段类型
        self.type = None if 'TYPE' not in p_field_def else p_field_def["TYPE"]

        # 字段是否显示
        self.display = None if 'DISPLAY' not in p_field_def else p_field_def["DISPLAY"]

        # 字段是否可显示
        self.edit = None if 'EDIT' not in p_field_def else p_field_def["EDIT"]

        # 字段是否可查询
        self.search = None if 'SEARCH' not in p_field_def else p_field_def["SEARCH"]

        # 字段是否在新增中显示
        self.add = None if 'ADD' not in p_field_def else p_field_def["ADD"]

        # 字段在新增是是否必填字段
        self.essential = None if 'ESSENTIAL' not in p_field_def else p_field_def["ESSENTIAL"]


class ViewDefinition(object):
    """
    表定义
    """
    def __init__(self, p_flag=None):

        # 字段定义
        self.fields = list()

        # 显示的字段定义
        self.fields_display = list()

        # 表原始定义
        self._def = list()

        # 下拉框定义
        self.select_def = dict()

        # 字典资源
        self._resource_dict = OrcResource("Dict")

        # log
        self._logger = OrcLog("view.lib.view_def")

        # 预定义表通过预定义数据定义,动态表要由输入参数给定定义
        if isinstance(p_flag, list):
            self._def = p_flag
        elif p_flag in rel_list:
            self._def = rel_list[p_flag]
        else:
            pass

        self._get_definition()

    @property
    def display_length(self):
        return len(self.fields_display)

    def get_field_by_index(self, p_index):
        """
        通过索引获取字段定义
        :param p_index:
        :return:
        """
        try:
            return self.fields[p_index]
        except IndexError:
            self._logger.error("field index is out of range.")

        return None

    def get_field_display_by_index(self, p_index):
        """
        通过索引获取可显示字段定义
        :param p_index:
        :return:
        """
        try:
            return self.fields_display[p_index]
        except IndexError:
            self._logger.error("field index is out of range.")

        return None

    def get_field_by_id(self, p_id):
        """
        通过 id 获取字段定义
        :param p_id:
        :return:
        """
        for _field in self.fields:
            if p_id == _field.id:
                return _field

        return None

    def _get_definition(self):
        """
         生成表定义
        :return:
        """
        # 生成列定义及显示的列
        for _field_def in self._def:

            _field = FieldDefinition(_field_def)
            self.fields.append(_field)

            if _field.display:

                self.fields_display.append(_field)

                if 'SELECT' == _field.type:
                    self._get_select_definition(_field.id)

                elif _field.type in ('TYPE_SELECT',):
                    self._get_complex_definition(_field.id)

    def _get_complex_definition(self, p_id):
        """

        :param p_id:
        :return:
        """
        self.select_def[p_id] = dict()

        _res = self._resource_dict.get(parameter=dict(TYPE='widget_type', DATA=dict()))

        if not ResourceCheck.result_status(_res, u"获取字典值", self._logger):
            self._logger.error("get dict %s failed." % p_id)
            return

        self.select_def[p_id].update({item['type_name']: item['type_text'] for item in _res.data})

    def _get_select_definition(self, p_id):
        """
        生成下拉列表定义
        :param p_id:
        :return:
        """
        self.select_def[p_id] = dict()

        def get_def(p_def_id):

            _res = self._resource_dict.get(parameter=dict(dict_flag=p_def_id))
            if not ResourceCheck.result_status(_res, u"获取字典值", self._logger):
                self._logger.error("get dict %s failed." % p_id)
                return

            self.select_def[p_id].update({item['dict_value']: item['dict_text'] for item in _res.data})

        if p_id in multi_select_definition:
            self.select_def[p_id] = dict()
            for _id in multi_select_definition[p_id]:
                get_def(_id)
        else:
            get_def(p_id)

def_view_batch_def = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="pid", NAME=u"父ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="batch_no", NAME=u"批编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=False, ESSENTIAL=False),
    dict(ID="batch_type", NAME=u"批类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="batch_name", NAME=u"批名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="batch_desc", NAME=u"批描述", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_batch_det = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="case_id", NAME=u"用例ID", TYPE="LINETEXT", DISPLAY=False, EDIT=True,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="case_no", NAME=u"用例编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="case_name", NAME=u"用例名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_case_def = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="pid", NAME=u"父ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="case_no", NAME=u"用例编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=False, ESSENTIAL=False),
    dict(ID="case_path", NAME=u"用例路径", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="case_name", NAME=u"用例名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="case_type", NAME=u"用例类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="case_desc", NAME=u"用例描述", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_step = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="step_no", NAME=u"步骤编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=False, ESSENTIAL=True),
    dict(ID="step_type", NAME=u"步骤类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="step_desc", NAME=u"步骤描述", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_item = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="item_no", NAME=u"条目编号", TYPE="LINETEXT", DISPLAY=True, EDIT=False,
         SEARCH=True, ADD=False, ESSENTIAL=False),
    dict(ID="item_type", NAME=u"条目类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="item_mode", NAME=u"条目模式", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="item_operate", NAME=u"条目操作", TYPE="OPE_DISP", DISPLAY=True, EDIT=False,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="item_desc", NAME=u"条目描述", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_page_def = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="page_flag", NAME=u"页面标识", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="page_desc", NAME=u"页面描述", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_page_det = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="page_id", NAME=u"页面ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="test_env", NAME=u"环境", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="page_url", NAME=u"URL", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

# DataDef 界面
def_view_data = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT",
         DISPLAY=False, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="test_env", NAME=u"测试环境", TYPE="SELECT",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="src_type", NAME=u"作用域类型", TYPE="SELECT",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="src_id", NAME=u"作用域标识", TYPE="DISPLAY",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=True, ESSENTIAL=True),
    dict(ID="data_flag", NAME=u"数据标识", TYPE="DISPLAY",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=True, ESSENTIAL=True),
    dict(ID="data_order", NAME=u"数据顺序", TYPE="LINETEXT",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=False, ESSENTIAL=False),
    dict(ID="data_mode", NAME=u"数据类型", TYPE="SELECT",
         DISPLAY=False, EDIT=False, SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="data_src_type", NAME=u"数据源", TYPE="DATASRC",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="data_value", NAME=u"数据", TYPE="TEXTAREA",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA",
         DISPLAY=True, EDIT=True, SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False)]

# DataSrc 界面
def_view_data_src = [
    dict(ID="id", NAME=u"序号", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="name", NAME=u"名称", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="desc", NAME=u"描述", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_run_time = [
    dict(ID="id", NAME=u"序号", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="module", NAME=u"模块", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="data_flag", NAME=u"数据标识", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="data_index", NAME=u"序号", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="data_value", NAME=u"数值", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False)]

# WidgetDef 界面定义
def_view_widget_def = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT",
         DISPLAY=False, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="pid", NAME=u"父ID", TYPE="LINETEXT",
         DISPLAY=False, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="widget_flag", NAME=u"控件标识", TYPE="LINETEXT",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="widget_path", NAME=u"控件路径", TYPE="LINETEXT",
         DISPLAY=False, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="widget_type", NAME=u"控件类型", TYPE="TYPE_SELECT",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="widget_desc", NAME=u"控件描述", TYPE="LINETEXT",
         DISPLAY=True, EDIT=True, SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA",
         DISPLAY=True, EDIT=True, SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_widget_det = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="widget_id", NAME=u"控件ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="widget_order", NAME=u"属性顺序", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=False, ESSENTIAL=False),
    dict(ID="widget_attr_type", NAME=u"属性类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="widget_attr_value", NAME=u"属性值", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="widget_desc", NAME=u"属性描述描述", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_window_def = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="window_flag", NAME=u"窗口标识", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="window_mark", NAME=u"标识控件", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="window_desc", NAME=u"窗口描述", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA", DISPLAY=True, EDIT=True,
         SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

def_view_run_def = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="pid", NAME=u"PID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="run_flag", NAME=u"名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="run_def_type", NAME=u"类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True)]

def_view_run_det = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="pid", NAME=u"PID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="flag", NAME=u"名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="run_det_type", NAME=u"类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="desc", NAME=u"描述", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="status", NAME=u"状态", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True)]

def_view_conf_menu = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="pid", NAME=u"PID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="name", NAME=u"名称", TYPE="LINETEXT", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

rel_list = dict(
    BatchDef=def_view_batch_def,
    BatchDet=def_view_batch_det,
    Case=def_view_case_def,
    Step=def_view_step,
    Item=def_view_item,
    Data=def_view_data,
    DataSrc=def_view_data_src,
    RunTime=def_view_run_time,
    PageDef=def_view_page_def,
    PageDet=def_view_page_det,
    WidgetDef=def_view_widget_def,
    WidgetDet=def_view_widget_det,
    Window=def_view_window_def,
    RunDef=def_view_run_def,
    RunDet=def_view_run_det,
    ConfMenu=def_view_conf_menu)

multi_select_definition = dict(
    run_def_type=('batch_type', 'case_type', 'run_def'),
    run_det_type=('batch_type', 'case_type', 'step_type', 'item_type')
)
