# coding=utf-8
from OrcLib.LibProgram import OrcFactory
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck


class FieldDefinition(object):
    """
    字段定义
    """
    def __init__(self, p_field_def=None):

        data = OrcFactory.create_default_dict(p_field_def, False)

        # 字段 id
        self.id = data.value('ID')

        # 字段名称
        self.name = data.value('NAME')

        # 字段类型
        self.type = data.value('TYPE')

        # 字段是否显示
        self.display = data.value('DISPLAY')

        # 字段是否可显示
        self.edit = data.value('EDIT')

        # 字段是否可查询
        self.search = data.value('SEARCH')

        # 字段是否在新增中显示
        self.add = data.value('ADD')

        # 字段在新增是是否必填字段
        self.essential = data.value('ESSENTIAL')

    def set_displayable(self, p_flag):
        """
        设置字段可显示
        :param p_flag:
        :return:
        """
        if isinstance(p_flag, bool):
            self.display = p_flag

    def set_editable(self, p_flag):
        """
        设置字段可编辑
        :param p_flag:
        :return:
        """
        if isinstance(p_flag, bool):
            self.edit = p_flag

    def set_searchable(self, p_flag):
        """
        设置可查询
        :param p_flag:
        :return:
        """
        if isinstance(p_flag, bool):
            self.search = p_flag

    def set_addable(self, p_flag):
        """
        设置增加时显示
        :param p_flag:
        :return:
        """
        if isinstance(p_flag, bool):
            self.add = p_flag

    def set_essential(self, p_flag):
        """
        设置为增加是必须有数据字段
        :param p_flag:
        :return:
        """
        if isinstance(p_flag, bool):
            self.essential = p_flag

    def to_dict(self):
        """
        生成 dict
        :return:
        """
        return dict(
            ID=self.id,
            NAME=self.name,
            TYPE=self.type,
            DISPLAY=self.display,
            EDIT=self.edit,
            SEARCH=self.search,
            ADD=self.add,
            ESSENTIAL=self.essential
        )


class ViewDefinition(object):
    """
    表定义
    """
    def __init__(self, p_flag=None):

        # 表原始定义
        self._def = list()

        # 字段定义
        self.fields = OrcFactory.create_ordered_dict()

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

        self._load_definition()

    # 长度
    @property
    def length(self):
        return len(self.fields)

    # 显示属性
    @property
    def length_display(self):
        return len(self.display_keys)

    @property
    def display_keys(self):
        return [item for item in self.fields.keys() if self.field(item).display]

    # 查询属性
    @property
    def length_search(self):
        return len(self.search_keys)

    @property
    def search_keys(self):
        return [item for item in self.fields.keys() if self.field(item).search]

    # 新增属性
    @property
    def length_add(self):
        return len(self.add_keys)

    @property
    def add_keys(self):
        return [item for item in self.fields.keys() if self.field(item).add]

    # 必须字段
    @property
    def essential_keys(self):
        return [item for item in self.fields.keys() if self.field(item).essential]

    def get_field_by_index(self, p_index):
        """
        通过索引获取字段定义
        :param p_index:
        :return:
        """
        return self.fields.value_by_index(p_index)

    def get_field_display(self, p_index):
        """
        通过索引获取可显示字段定义
        :param p_index:
        :return:
        """
        return self.field(self.display_keys[p_index])

    def get_field_search(self, p_index):
        """
        通过索引获取可显示字段定义
        :param p_index:
        :return:
        """
        return self.field(self.search_keys[p_index])

    def get_field_add(self, p_index):
        """
        通过索引获取可显示字段定义
        :param p_index:
        :return:
        """
        return self.field(self.add_keys[p_index])

    def field(self, p_id):
        """
        通过 id 获取字段定义
        :param p_id:
        :return:
        :rtype: FieldDefinition
        """
        if p_id in self.fields.keys():
            return self.fields.value(p_id)
        else:
            return FieldDefinition()

    def _load_definition(self):
        """
         生成表定义
        :return:
        """
        # 生成列定义及显示的列
        for _field_data in self._def:

            _field = FieldDefinition(_field_data)
            self.fields.append(_field.id, _field)

            if 'SELECT' == _field.type:
                self._load_select(_field.id)

            elif _field.type in ('TYPE_SELECT',):
                self._load_complex(_field.id)

            else:
                pass

    def _load_complex(self, p_id):
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

    def _load_select(self, p_id):
        """
        生成下拉框定义
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

    def to_dict(self):
        """
        输出 dict
        :return:
        """
        return [self.field(_key).to_dict() for _key in self.fields.keys()]


view_batch_def = [
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

view_batch_det = [
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

view_case_def = [
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

view_step = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="step_no", NAME=u"步骤编号", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=False, ESSENTIAL=False),
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

view_item = [
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

view_page_def = [
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

view_page_det = [
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
view_data = [
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
view_data_src = [
    dict(ID="id", NAME=u"序号", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="name", NAME=u"名称", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="desc", NAME=u"描述", TYPE="LINETEXT",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False)]

view_run_time = [
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
view_widget_def = [
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

view_widget_det = [
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

view_window_def = [
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

view_run_def = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="pid", NAME=u"PID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="run_flag", NAME=u"名称", TYPE="LINETEXT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="run_def_type", NAME=u"类型", TYPE="SELECT", DISPLAY=True, EDIT=True,
         SEARCH=True, ADD=True, ESSENTIAL=True)]

view_run_det = [
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

view_conf_menu = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="pid", NAME=u"PID", TYPE="LINETEXT", DISPLAY=False, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="name", NAME=u"名称", TYPE="LINETEXT", DISPLAY=True, EDIT=False,
         SEARCH=False, ADD=False, ESSENTIAL=False)]

# 数据标识界面定义,用于运行调试界面及数据新增,只读表,没有增删改
view_data_flag = [
    # 使用 item 界面的 item_id
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT", DISPLAY=False),

    # 标识,WEB 用控件标识, DATA 用 data_id
    dict(ID="flag", NAME=u"标识", TYPE="LINETEXT", DISPLAY=True),

    # 类型,条目类型 WEB/DATA
    dict(ID="data_flag_type", NAME=u"类型", TYPE="SELECT", DISPLAY=True),

    # 模式
    dict(ID="item_mode", NAME=u"模式", TYPE="SELECT", DISPLAY=True),

    # 数据个数
    dict(ID="num", NAME=u"数量", TYPE="LINETEXT", DISPLAY=True),

    # 描述
    dict(ID="desc", NAME=u"描述", TYPE="LINETEXT", DISPLAY=True)]

rel_list = dict(
    BatchDef=view_batch_def,
    BatchDet=view_batch_det,
    Case=view_case_def,
    Step=view_step,
    Item=view_item,
    Data=view_data,
    DataSrc=view_data_src,
    RunTime=view_run_time,
    PageDef=view_page_def,
    PageDet=view_page_det,
    WidgetDef=view_widget_def,
    WidgetDet=view_widget_det,
    Window=view_window_def,
    RunDef=view_run_def,
    RunDet=view_run_det,
    ConfMenu=view_conf_menu,
    DataFlag=view_data_flag)

multi_select_definition = dict(
    run_def_type=('batch_type', 'case_type', 'run_def'),
    run_det_type=('batch_type', 'case_type', 'step_type', 'item_type'),
    data_flag_type=('operate_object_type', 'item_type')
)
