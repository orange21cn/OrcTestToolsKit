# coding=utf-8

# DataDef 界面
view_data_def = [
    dict(ID="id", NAME=u"ID", TYPE="LINETEXT",
         DISPLAY=False, EDIT=False, SEARCH=False, ADD=False, ESSENTIAL=False),
    dict(ID="test_env", NAME=u"测试环境", TYPE="SELECT",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="src_type", NAME=u"作用域类型", TYPE="SELECT",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="src_id", NAME=u"作用域标识", TYPE="LINETEXT",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=True),
    dict(ID="data_flag", NAME=u"数据标识", TYPE="LINETEXT",
         DISPLAY=True, EDIT=True, SEARCH=True, ADD=True, ESSENTIAL=True),
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
view_widget_def = [
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
