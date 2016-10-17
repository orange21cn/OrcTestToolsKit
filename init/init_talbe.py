# coding=utf-8
from OrcApi import orc_db

from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import LibSequence

from OrcLib.LibDatabase import LibWidgetType
from OrcLib.LibDatabase import LibWidgetOperation

init_value_dictionary = [
    LibDictionary(dict(id="10001", dict_flag="case_type", dict_order="1", dict_value="GROUP", dict_text=u"用例组", dict_desc=u"用于存放批量用例")),
    LibDictionary(dict(id="10002", dict_flag="case_type", dict_order="2", dict_value="CASE", dict_text=u"用例", dict_desc=u"单个用例")),
    LibDictionary(dict(id="10003", dict_flag="data_mode", dict_order="1", dict_value="STR", dict_text=u"字符", dict_desc="")),
    LibDictionary(dict(id="10004", dict_flag="data_mode", dict_order="2", dict_value="INT", dict_text=u"整数", dict_desc="")),
    LibDictionary(dict(id="10005", dict_flag="data_mode", dict_order="3", dict_value="SQL", dict_text="SQL", dict_desc="")),
    LibDictionary(dict(id="10006", dict_flag="data_type", dict_order="1", dict_value="INP", dict_text=u"输入", dict_desc="")),
    LibDictionary(dict(id="10007", dict_flag="data_type", dict_order="2", dict_value="OUT", dict_text=u"输出", dict_desc="")),
    LibDictionary(dict(id="10008", dict_flag="data_type", dict_order="3", dict_value="CHK", dict_text=u"检查", dict_desc="")),
    LibDictionary(dict(id="10009", dict_flag="item_type", dict_order="1", dict_value="WEB", dict_text="WEB", dict_desc="")),
    LibDictionary(dict(id="10010", dict_flag="item_type", dict_order="2", dict_value="IOS", dict_text="IOS", dict_desc="")),
    LibDictionary(dict(id="10011", dict_flag="item_type", dict_order="3", dict_value="ANDROID", dict_text="ANDROID", dict_desc="")),
    LibDictionary(dict(id="10012", dict_flag="item_type", dict_order="4", dict_value="JSON", dict_text=u"JSON接口", dict_desc="")),
    LibDictionary(dict(id="10013", dict_flag="item_type", dict_order="5", dict_value="WEBSERVICE", dict_text="WEBSERVICE", dict_desc="")),
    LibDictionary(dict(id="10014", dict_flag="item_mode", dict_order="1", dict_value="OPERATE", dict_text=u"操作项", dict_desc=u"执行操作")),
    LibDictionary(dict(id="10015", dict_flag="item_mode", dict_order="2", dict_value="CHECK", dict_text=u"检查项", dict_desc=u"执行检查")),
    LibDictionary(dict(id="10016", dict_flag="widget_operator", dict_order="1", dict_value="INPUT", dict_text=u"输入", dict_desc="")),
    LibDictionary(dict(id="10017", dict_flag="widget_operator", dict_order="2", dict_value="SUBMIT", dict_text=u"点击", dict_desc="")),
    LibDictionary(dict(id="10018", dict_flag="widget_type", dict_order="1", dict_value="WINDOW", dict_text=u"窗口", dict_desc="")),
    LibDictionary(dict(id="10019", dict_flag="widget_type", dict_order="2", dict_value="FRAME", dict_text="FRAME", dict_desc="")),
    LibDictionary(dict(id="10020", dict_flag="widget_type", dict_order="3", dict_value="INP", dict_text=u"输入框", dict_desc="")),
    LibDictionary(dict(id="10021", dict_flag="widget_type", dict_order="4", dict_value="BTN", dict_text=u"按钮", dict_desc="")),
    LibDictionary(dict(id="10022", dict_flag="widget_type", dict_order="5", dict_value="LINK", dict_text=u"链接", dict_desc="")),
    LibDictionary(dict(id="10023", dict_flag="widget_type", dict_order="6", dict_value="SPAN", dict_text="SPAN", dict_desc="")),
    LibDictionary(dict(id="10024", dict_flag="widget_attr_type", dict_order="1", dict_value="ID", dict_text="ID", dict_desc="")),
    LibDictionary(dict(id="10025", dict_flag="widget_attr_type", dict_order="2", dict_value="NAME", dict_text="NAME", dict_desc="")),
    LibDictionary(dict(id="10026", dict_flag="widget_attr_type", dict_order="3", dict_value="XPATH", dict_text="XPATH", dict_desc="")),
    LibDictionary(dict(id="10027", dict_flag="widget_attr_type", dict_order="4", dict_value="TAGNAME", dict_text="TAGNAME", dict_desc="")),
    LibDictionary(dict(id="10028", dict_flag="src_type", dict_order="1", dict_value="BATCH", dict_text=u"批", dict_desc="")),
    LibDictionary(dict(id="10029", dict_flag="src_type", dict_order="2", dict_value="CASE", dict_text=u"用例", dict_desc="")),
    LibDictionary(dict(id="10030", dict_flag="src_type", dict_order="3", dict_value="STEP", dict_text=u"步骤", dict_desc="")),
    LibDictionary(dict(id="10031", dict_flag="src_type", dict_order="4", dict_value="ITEM", dict_text=u"执行项", dict_desc="")),
    LibDictionary(dict(id="10032", dict_flag="operate_object_type", dict_order="1", dict_value="PAGE", dict_text=u"页面", dict_desc="")),
    LibDictionary(dict(id="10033", dict_flag="operate_object_type", dict_order="2", dict_value="WIDGET", dict_text=u"控件", dict_desc="")),
    LibDictionary(dict(id="10034", dict_flag="page_operator", dict_order="1", dict_value="GET", dict_text=u"打开", dict_desc=""))]


init_value_sequence = [
    LibSequence(dict(id="20001", field_name="batch_def", field_seq="1000000000")),
    LibSequence(dict(id="20002", field_name="batch_det", field_seq="1100000000")),
    LibSequence(dict(id="20003", field_name="case_def", field_seq="2000000000")),
    LibSequence(dict(id="20004", field_name="case_det", field_seq="2100000000")),
    LibSequence(dict(id="20005", field_name="step_def", field_seq="2200000000")),
    LibSequence(dict(id="20006", field_name="step_det", field_seq="2300000000")),
    LibSequence(dict(id="20007", field_name="item", field_seq="2400000000")),
    LibSequence(dict(id="20008", field_name="page_def", field_seq="3000000000")),
    LibSequence(dict(id="20009", field_name="page_det", field_seq="3100000000")),
    LibSequence(dict(id="20010", field_name="window_def", field_seq="3200000000")),
    LibSequence(dict(id="20011", field_name="widget_def", field_seq="3300000000")),
    LibSequence(dict(id="20012", field_name="widget_det", field_seq="3400000000")),
    LibSequence(dict(id="20013", field_name="data", field_seq="4000000000"))]

init_value_widget_type = [
    LibWidgetType(dict(id="30001", type_order=1, type_mode="PRO", type_name="WINDOW", type_text=u"窗口", type_desc="")),
    LibWidgetType(dict(id="30002", type_order=2, type_mode="PRO", type_name="FRAME", type_text="FRAME", type_desc="")),
    LibWidgetType(dict(id="30003", type_order=3, type_mode="PRO", type_name="INP", type_text=u"输入框", type_desc="")),
    LibWidgetType(dict(id="30004", type_order=4, type_mode="PRO", type_name="BTN", type_text=u"按钮", type_desc="")),
    LibWidgetType(dict(id="30005", type_order=5, type_mode="PRO", type_name="LINK", type_text=u"链接", type_desc="")),
    LibWidgetType(dict(id="30006", type_order=6, type_mode="PRO", type_name="SPAN", type_text="SPAN", type_desc="")),
    LibWidgetType(dict(id="30007", type_order=7, type_mode="USR", type_name="TEST", type_text="TEST", type_desc=u"测试用"))]

init_value_widget_operation = [
    LibWidgetOperation(dict(id="40001", type_name="FRAME", ope_order="1", ope_name="EXISTS", ope_text=u"存在", ope_desc="")),
    LibWidgetOperation(dict(id="40002", type_name="INP", ope_order="1", ope_name="EXISTS", ope_text=u"存在", ope_desc="")),
    LibWidgetOperation(dict(id="40003", type_name="INP", ope_order="2", ope_name="INPUT", ope_text=u"输入", ope_desc="")),
    LibWidgetOperation(dict(id="40004", type_name="BTN", ope_order="1", ope_name="EXISTS", ope_text=u"存在", ope_desc="")),
    LibWidgetOperation(dict(id="40005", type_name="BTN", ope_order="2", ope_name="CLICK", ope_text=u"点击", ope_desc="")),
    LibWidgetOperation(dict(id="40006", type_name="LINK", ope_order="1", ope_name="EXISTS", ope_text=u"存在", ope_desc="")),
    LibWidgetOperation(dict(id="40007", type_name="LINK", ope_order="2", ope_name="CLICK", ope_text=u"点击", ope_desc="")),
    LibWidgetOperation(dict(id="40008", type_name="SPAN", ope_order="1", ope_name="EXISTS", ope_text=u"存在", ope_desc=""))]

orc_db.drop_all()
orc_db.create_all()

orc_db.session.add_all(init_value_widget_type)
orc_db.session.add_all(init_value_widget_operation)
orc_db.session.add_all(init_value_dictionary)
orc_db.session.add_all(init_value_sequence)

orc_db.session.commit()
