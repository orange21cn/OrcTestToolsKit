# coding=utf-8
from OrcLib.LibLog import OrcLog

_logger = OrcLog("view.basic.view_def")


class FieldDefinition(object):
    """
    字段定义
    """
    def __init__(self, p_field_def):

        # 字段 id
        self.id = p_field_def["ID"]

        # 字段名称
        self.name = p_field_def["NAME"]

        # 字段类型
        self.type = p_field_def["TYPE"]

        # 字段是否显示
        self.display = p_field_def["DISPLAY"]

        # 字段是否可显示
        self.edit = p_field_def["EDIT"]

        # 字段是否可查询
        self.search = p_field_def["SEARCH"]

        # 字段是否在新增中显示
        self.add = p_field_def["ADD"]

        # 字段在新增是是否必填字段
        self.essential = p_field_def["ESSENTIAL"]


class ViewDefinition(object):
    """
    表定义
    """
    def __init__(self, p_flag):

        self.fields = list()
        self.fields_display = list()

        self._def = list()

        if "BatchDef" == p_flag:
            self._def = def_view_batch_def
        elif "BatchDet" == p_flag:
            self._def = def_view_batch_det
        elif "Case" == p_flag:
            self._def = def_view_case_def
        elif "Step" == p_flag:
            self._def = def_view_step
        elif "Item" == p_flag:
            self._def = def_view_item
        elif "Data" == p_flag:
            self._def = def_view_data
        elif "PageDef" == p_flag:
            self._def = def_view_page_def
        elif "PageDet" == p_flag:
            self._def = def_view_page_det
        elif "WidgetDef" == p_flag:
            self._def = def_view_widget_def
        elif "WidgetDet" == p_flag:
            self._def = def_view_widget_det
        elif "Window" == p_flag:
            self._def = def_view_window_def
        elif "RunDef" == p_flag:
            self._def = def_view_run_def
        elif "RunDet" == p_flag:
            self._def = def_view_run_det
        else:
            pass

        for _field_def in self._def:

            _field = FieldDefinition(_field_def)

            self.fields.append(_field)

            if _field.display:
                self.fields_display.append(_field)

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
            _logger.error("field index is out of range.")

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
            _logger.error("field index is out of range.")

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
    dict(ID="item_operate", NAME=u"条目操作", TYPE="OPERATE", DISPLAY=True, EDIT=False,
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
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="data_value", NAME=u"数据", TYPE="TEXTAREA",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=False),
    dict(ID="comment", NAME=u"备注", TYPE="TEXTAREA",
         DISPLAY=True, EDIT=True, SEARCH=False, ADD=True, ESSENTIAL=False),
    dict(ID="create_time", NAME=u"创建时间", TYPE="DATETIME",
         DISPLAY=True, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="modify_time", NAME=u"修改时间", TYPE="DATETIME",
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
    dict(ID="widget_type", NAME=u"控件类型", TYPE="SEL_WIDGET",
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
