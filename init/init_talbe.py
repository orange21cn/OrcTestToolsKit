# coding=utf-8
from OrcApi import orc_db

from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import LibSequence

init_value_dictionary = [
    LibDictionary(dict(id="1", dict_flag="case_type", dict_order="1", dict_value="GROUP", dict_text=u"用例组", dict_desc=u"用于存放批量用例")),
    LibDictionary(dict(id="2", dict_flag="case_type", dict_order="2", dict_value="CASE", dict_text=u"用例", dict_desc=u"单个用例")),
    LibDictionary(dict(id="3", dict_flag="data_mode", dict_order="1", dict_value="STR", dict_text=u"字符", dict_desc="")),
    LibDictionary(dict(id="4", dict_flag="data_mode", dict_order="2", dict_value="INT", dict_text=u"整数", dict_desc="")),
    LibDictionary(dict(id="5", dict_flag="data_mode", dict_order="3", dict_value="SQL", dict_text="SQL", dict_desc="")),
    LibDictionary(dict(id="6", dict_flag="data_type", dict_order="1", dict_value="INP", dict_text=u"输入", dict_desc="")),
    LibDictionary(dict(id="7", dict_flag="data_type", dict_order="2", dict_value="OUT", dict_text=u"输出", dict_desc="")),
    LibDictionary(dict(id="8", dict_flag="data_type", dict_order="3", dict_value="CHK", dict_text=u"检查", dict_desc="")),
    LibDictionary(dict(id="9", dict_flag="item_type", dict_order="1", dict_value="WEB", dict_text="WEB", dict_desc="")),
    LibDictionary(dict(id="10", dict_flag="item_type", dict_order="2", dict_value="IOS", dict_text="IOS", dict_desc="")),
    LibDictionary(dict(id="11", dict_flag="item_type", dict_order="3", dict_value="ANDROID", dict_text="ANDROID", dict_desc="")),
    LibDictionary(dict(id="12", dict_flag="item_type", dict_order="4", dict_value="JSON", dict_text=u"JSON接口", dict_desc="")),
    LibDictionary(dict(id="13", dict_flag="item_type", dict_order="5", dict_value="WEBSERVICE", dict_text="WEBSERVICE", dict_desc="")),
    LibDictionary(dict(id="14", dict_flag="item_mode", dict_order="1", dict_value="OPERATE", dict_text=u"操作项", dict_desc=u"执行操作")),
    LibDictionary(dict(id="15", dict_flag="item_mode", dict_order="2", dict_value="CHECK", dict_text=u"检查项", dict_desc=u"执行检查")),
    LibDictionary(dict(id="16", dict_flag="widget_operator", dict_order="1", dict_value="INPUT", dict_text=u"输入", dict_desc="")),
    LibDictionary(dict(id="17", dict_flag="widget_operator", dict_order="2", dict_value="SUBMIT", dict_text=u"点击", dict_desc="")),
    LibDictionary(dict(id="18", dict_flag="widget_type", dict_order="1", dict_value="WINDOW", dict_text=u"窗口", dict_desc="")),
    LibDictionary(dict(id="19", dict_flag="widget_type", dict_order="2", dict_value="FRAME", dict_text="FRAME", dict_desc="")),
    LibDictionary(dict(id="20", dict_flag="widget_type", dict_order="3", dict_value="INP", dict_text=u"输入框", dict_desc="")),
    LibDictionary(dict(id="21", dict_flag="widget_type", dict_order="4", dict_value="BTN", dict_text=u"按钮", dict_desc="")),
    LibDictionary(dict(id="22", dict_flag="widget_type", dict_order="5", dict_value="LINK", dict_text=u"链接", dict_desc="")),
    LibDictionary(dict(id="23", dict_flag="widget_type", dict_order="6", dict_value="SPAN", dict_text="SPAN", dict_desc="")),
    LibDictionary(dict(id="24", dict_flag="widget_attr_type", dict_order="1", dict_value="ID", dict_text="ID", dict_desc="")),
    LibDictionary(dict(id="25", dict_flag="widget_attr_type", dict_order="2", dict_value="NAME", dict_text="NAME", dict_desc="")),
    LibDictionary(dict(id="26", dict_flag="widget_attr_type", dict_order="3", dict_value="XPATH", dict_text="XPATH", dict_desc="")),
    LibDictionary(dict(id="27", dict_flag="widget_attr_type", dict_order="4", dict_value="TAGNAME", dict_text="TAGNAME", dict_desc="")),
    LibDictionary(dict(id="28", dict_flag="src_type", dict_order="1", dict_value="BATCH", dict_text=u"批", dict_desc="")),
    LibDictionary(dict(id="29", dict_flag="src_type", dict_order="2", dict_value="CASE", dict_text=u"用例", dict_desc="")),
    LibDictionary(dict(id="30", dict_flag="src_type", dict_order="3", dict_value="STEP", dict_text=u"步骤", dict_desc="")),
    LibDictionary(dict(id="31", dict_flag="src_type", dict_order="4", dict_value="ITEM", dict_text=u"执行项", dict_desc="")),
    LibDictionary(dict(id="32", dict_flag="operate_object_type", dict_order="1", dict_value="PAGE", dict_text=u"页面", dict_desc="")),
    LibDictionary(dict(id="33", dict_flag="operate_object_type", dict_order="2", dict_value="WIDGET", dict_text=u"控件", dict_desc="")),
    LibDictionary(dict(id="34", dict_flag="page_operator", dict_order="1", dict_value="GET", dict_text=u"打开", dict_desc=""))]


init_value_sequence = [
    LibSequence(dict(id="10001", field_name="batch_def", field_seq="1000000000")),
    LibSequence(dict(id="10002", field_name="batch_det", field_seq="1100000000")),
    LibSequence(dict(id="10003", field_name="case_def", field_seq="2000000000")),
    LibSequence(dict(id="10004", field_name="case_det", field_seq="2100000000")),
    LibSequence(dict(id="10005", field_name="step_def", field_seq="2200000000")),
    LibSequence(dict(id="10006", field_name="step_det", field_seq="2300000000")),
    LibSequence(dict(id="10007", field_name="item", field_seq="2400000000")),
    LibSequence(dict(id="10008", field_name="page_def", field_seq="3000000000")),
    LibSequence(dict(id="10009", field_name="page_det", field_seq="3100000000")),
    LibSequence(dict(id="10010", field_name="window_def", field_seq="3200000000")),
    LibSequence(dict(id="10011", field_name="widget_def", field_seq="3300000000")),
    LibSequence(dict(id="10012", field_name="widget_det", field_seq="3400000000")),
    LibSequence(dict(id="10013", field_name="data", field_seq="4000000000"))]

orc_db.drop_all()
orc_db.create_all()

orc_db.session.add_all(init_value_dictionary)
orc_db.session.add_all(init_value_sequence)
orc_db.session.commit()
