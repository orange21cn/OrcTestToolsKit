# coding=utf-8
from OrcApi import orc_db

from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import LibSequence

from OrcLib.LibDatabase import LibWidgetType
from OrcLib.LibDatabase import LibWidgetOperation


init_value_dictionary = [

    LibDictionary(dict(id="10101", dict_flag="batch_type", dict_order="1",
                       dict_value="BATCH_SUITE", dict_text=u"计划组", dict_param='', dict_desc=u"用于存放批量计划")),
    LibDictionary(dict(id="10102", dict_flag="batch_type", dict_order="2",
                       dict_value="BATCH", dict_text=u"计划", dict_param='', dict_desc=u"单个计划")),

    LibDictionary(dict(id="10201", dict_flag="case_type", dict_order="1",
                       dict_value="CASE_SUITE", dict_text=u"用例组", dict_param='', dict_desc=u"用于存放批量用例")),
    LibDictionary(dict(id="10202", dict_flag="case_type", dict_order="2",
                       dict_value="CASE", dict_text=u"用例", dict_param='', dict_desc=u"单个用例")),
    LibDictionary(dict(id="10203", dict_flag="case_type", dict_order="3",
                       dict_value="FUNC_SUITE", dict_text=u"函数组", dict_param='', dict_desc=u"函数组")),
    LibDictionary(dict(id="10204", dict_flag="case_type", dict_order="3",
                       dict_value="FUNC", dict_text=u"函数", dict_param='', dict_desc=u"用例但不能单独执行")),

    LibDictionary(dict(id="10301", dict_flag="step_type", dict_order="1",
                       dict_value="STEP_NORMAL", dict_text=u"普通步骤", dict_param='', dict_desc=u"普通步骤")),
    LibDictionary(dict(id="10302", dict_flag="step_type", dict_order="1",
                       dict_value="STEP_FUNC", dict_text=u"函数步骤", dict_param='', dict_desc=u"函数步骤")),

    LibDictionary(dict(id="10401", dict_flag="item_type", dict_order="1",
                       dict_value="WEB", dict_text="WEB", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10402", dict_flag="item_type", dict_order="2",
                       dict_value="DATA", dict_text=u"数据", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10403", dict_flag="item_type", dict_order="3",
                       dict_value="IOS", dict_text="IOS", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10404", dict_flag="item_type", dict_order="4",
                       dict_value="ANDROID", dict_text="ANDROID", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10405", dict_flag="item_type", dict_order="5",
                       dict_value="JSON", dict_text=u"JSON接口", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10406", dict_flag="item_type", dict_order="6",
                       dict_value="WEBSERVICE", dict_text="WEBSERVICE", dict_param='', dict_desc="")),

    LibDictionary(dict(id="10501", dict_flag="item_mode", dict_order="1",
                       dict_value="OPERATE", dict_text=u"操作项", dict_param='', dict_desc=u"执行操作")),
    LibDictionary(dict(id="10502", dict_flag="item_mode", dict_order="2",
                       dict_value="CHECK", dict_text=u"检查项", dict_param='', dict_desc=u"执行检查")),

    LibDictionary(dict(id="10601", dict_flag="data_mode", dict_order="1",
                       dict_value="STR", dict_text=u"字符", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10602", dict_flag="data_mode", dict_order="2",
                       dict_value="INT", dict_text=u"整数", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10603", dict_flag="data_mode", dict_order="3",
                       dict_value="SQL", dict_text="SQL", dict_param='', dict_desc="")),

    LibDictionary(dict(id="10701", dict_flag="data_type", dict_order="1",
                       dict_value="INP", dict_text=u"输入", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10702", dict_flag="data_type", dict_order="2",
                       dict_value="OUT", dict_text=u"输出", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10703", dict_flag="data_type", dict_order="3",
                       dict_value="CHK", dict_text=u"检查", dict_param='', dict_desc="")),

    LibDictionary(dict(id="10801", dict_flag="widget_attr_type", dict_order="1",
                       dict_value="ID", dict_text="ID", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10802", dict_flag="widget_attr_type", dict_order="2",
                       dict_value="NAME", dict_text="NAME", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10803", dict_flag="widget_attr_type", dict_order="3",
                       dict_value="XPATH", dict_text="XPATH", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10804", dict_flag="widget_attr_type", dict_order="4",
                       dict_value="TAGNAME", dict_text=u"标签名称", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10805", dict_flag="widget_attr_type", dict_order="5",
                       dict_value="LINK_TEXT", dict_text=u"链接文字", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10806", dict_flag="widget_attr_type", dict_order="6",
                       dict_value="CSS", dict_text="CSS", dict_param='', dict_desc="")),

    LibDictionary(dict(id="10901", dict_flag="src_type", dict_order="1",
                       dict_value="BATCH", dict_text=u"计划", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10902", dict_flag="src_type", dict_order="2",
                       dict_value="CASE", dict_text=u"用例", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10903", dict_flag="src_type", dict_order="3",
                       dict_value="STEP", dict_text=u"步骤", dict_param='', dict_desc="")),
    LibDictionary(dict(id="10904", dict_flag="src_type", dict_order="4",
                       dict_value="ITEM", dict_text=u"执行项", dict_param='', dict_desc="")),

    LibDictionary(dict(id="11001", dict_flag="operate_object_type", dict_order="1",
                       dict_value="PAGE", dict_text=u"页面", dict_param='(\'operation\',)', dict_desc="")),
    LibDictionary(dict(id="11002", dict_flag="operate_object_type", dict_order="2",
                       dict_value="WINDOW", dict_text=u"窗口", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11003", dict_flag="operate_object_type", dict_order="3",
                       dict_value="WIDGET", dict_text=u"控件", dict_param='(\'operation\', \'check\')', dict_desc="")),

    # LibDictionary(dict(id="11003", dict_flag="run_def_type", dict_order="1",
    #                    dict_value="BATCH", dict_text=u"计划", dict_param='', dict_desc="")),
    # LibDictionary(dict(id="11004", dict_flag="run_def_type", dict_order="2",
    #                    dict_value="CASE", dict_text=u"用例", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11101", dict_flag="run_def", dict_order="3",
                       dict_value="TEST", dict_text=u"执行记录", dict_param='', dict_desc="")),

    LibDictionary(dict(id="11201", dict_flag="test_env", dict_order="1",
                       dict_value="TEST", dict_text=u"测试环境", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11202", dict_flag="test_env", dict_order="2",
                       dict_value="PRE", dict_text=u"预生产环境", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11203", dict_flag="test_env", dict_order="3",
                       dict_value="PRD", dict_text=u"生产环境", dict_param='', dict_desc="")),

    LibDictionary(dict(id="11301", dict_flag="browser", dict_order="1",
                       dict_value="FIREFOX", dict_text="FIREFOX", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11302", dict_flag="browser", dict_order="2",
                       dict_value="CHROME", dict_text="CHROME", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11303", dict_flag="browser", dict_order="3",
                       dict_value="IE", dict_text="IE", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11304", dict_flag="browser", dict_order="4",
                       dict_value="EDGE", dict_text="EDGE", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11305", dict_flag="browser", dict_order="5",
                       dict_value="PHANTOMJS", dict_text="PHANTOMJS", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11306", dict_flag="browser", dict_order="6",
                       dict_value="SAFARI", dict_text="SAFARI", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11307", dict_flag="browser", dict_order="7",
                       dict_value="HTMLUNIT", dict_text="HTMLUNIT", dict_param='', dict_desc="")),

    LibDictionary(dict(id="11401", dict_flag="data_src_type", dict_order="1",
                       dict_value="SQLite", dict_text="SQLite", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11402", dict_flag="data_src_type", dict_order="2",
                       dict_value="MySql", dict_text="MySql", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11403", dict_flag="data_src_type", dict_order="3",
                       dict_value="Oracle", dict_text="Oracle", dict_param='', dict_desc="")),

    LibDictionary(dict(id="11501", dict_flag="result", dict_order="1",
                       dict_value="PASS", dict_text=u"通过", dict_param='', dict_desc="")),
    LibDictionary(dict(id="11502", dict_flag="result", dict_order="2",
                       dict_value="FAIL", dict_text=u"失败", dict_param='', dict_desc=""))]


init_value_sequence = [
    LibSequence(dict(id="20001", field_name="batch_def", field_seq="100000000")),
    LibSequence(dict(id="20002", field_name="batch_det", field_seq="110000000")),
    LibSequence(dict(id="20003", field_name="case_def", field_seq="200000000")),
    LibSequence(dict(id="20004", field_name="case_det", field_seq="210000000")),
    LibSequence(dict(id="20005", field_name="step_def", field_seq="220000000")),
    LibSequence(dict(id="20006", field_name="step_det", field_seq="230000000")),
    LibSequence(dict(id="20007", field_name="item", field_seq="240000000")),
    LibSequence(dict(id="20008", field_name="page_def", field_seq="300000000")),
    LibSequence(dict(id="20009", field_name="page_det", field_seq="310000000")),
    LibSequence(dict(id="20010", field_name="window_def", field_seq="320000000")),
    LibSequence(dict(id="20011", field_name="widget_def", field_seq="330000000")),
    LibSequence(dict(id="20012", field_name="widget_det", field_seq="340000000")),
    LibSequence(dict(id="20013", field_name="data", field_seq="400000000")),
    LibSequence(dict(id="20014", field_name="dictionary", field_seq="20000")),
    LibSequence(dict(id="20015", field_name="widget_type", field_seq="21000")),
    LibSequence(dict(id="20016", field_name="widget_operation", field_seq="22000"))]

init_value_widget_type = [
    LibWidgetType(dict(id="30001", type_order=1, type_mode="PRO",
                       type_name="GROUP", type_text=u"控件组", type_desc="")),
    # LibWidgetType(dict(id="30002", type_order=2, type_mode="PRO",
    #                    type_name="PAGE", type_text=u"页面", type_desc="")),
    # LibWidgetType(dict(id="30003", type_order=3, type_mode="PRO",
    #                    type_name="WINDOW", type_text=u"窗口", type_desc="")),
    LibWidgetType(dict(id="30004", type_order=4, type_mode="PRO",
                       type_name="FRAME", type_text=u"FRAME", type_desc="")),
    LibWidgetType(dict(id="30005", type_order=5, type_mode="PRO",
                       type_name="BLOCK", type_text=u"块", type_desc="")),
    LibWidgetType(dict(id="30006", type_order=6, type_mode="PRO",
                       type_name="INP", type_text=u"输入框", type_desc="")),
    LibWidgetType(dict(id="30007", type_order=7, type_mode="PRO",
                       type_name="BTN", type_text=u"按钮", type_desc="")),
    LibWidgetType(dict(id="30008", type_order=8, type_mode="PRO",
                       type_name="LINK", type_text=u"链接", type_desc="")),
    LibWidgetType(dict(id="30009", type_order=9, type_mode="PRO",
                       type_name="SELECT", type_text=u"下拉框", type_desc="")),
    LibWidgetType(dict(id="30010", type_order=10, type_mode="PRO",
                       type_name="ALERT", type_text=u"提示框", type_desc=""))]
    # LibWidgetType(dict(id="31000", type_order=8, type_mode="USR",
    #                    type_name="TEST", type_text="TEST", type_desc=u"测试用"))]

init_value_widget_operation = [
    LibWidgetOperation(dict(id="40001", type_name="PAGE", ope_order="1", ope_name="GET", ope_text=u"打开",
                            operate_text=u"打开", check_text=u"", ope_desc=u"")),
    LibWidgetOperation(dict(id="40002", type_name="PAGE", ope_order="2", ope_name="MAX", ope_text=u"最大化",
                            operate_text=u"最大化", check_text=u"", ope_desc=u"")),

    LibWidgetOperation(dict(id="40101", type_name="BLOCK", ope_order="1", ope_name="EXISTS", ope_text=u"存在",
                            operate_text=u"", check_text=u"检查存在", ope_desc=u"")),
    LibWidgetOperation(dict(id="40102", type_name="BLOCK", ope_order="2", ope_name="CLICK", ope_text=u"点击",
                            operate_text=u"点击", check_text=u"", ope_desc=u"")),
    LibWidgetOperation(dict(id="40103", type_name="BLOCK", ope_order="3", ope_name="GET_ATTR", ope_text=u"获取属性",
                            operate_text=u"", check_text=u"检查属性", ope_desc=u"")),
    LibWidgetOperation(dict(id="40104", type_name="BLOCK", ope_order="4", ope_name="GET_TEXT", ope_text=u"获取文本",
                            operate_text=u"", check_text=u"检查文本", ope_desc=u"")),
    LibWidgetOperation(dict(id="40105", type_name="BLOCK", ope_order="5", ope_name="GET_HTML", ope_text=u"获取HTML",
                            operate_text=u"", check_text=u"", ope_desc=u"")),
    LibWidgetOperation(dict(id="40106", type_name="BLOCK", ope_order="6", ope_name="SCROLL", ope_text=u"滚动至显示",
                            operate_text=u"滚动至显示", check_text=u"", ope_desc=u"")),
    LibWidgetOperation(dict(id="40107", type_name="BLOCK", ope_order="7", ope_name="FOCUS", ope_text=u"焦点至",
                            operate_text=u"焦点至", check_text=u"", ope_desc=u"")),

    LibWidgetOperation(dict(id="40201", type_name="SELECT", ope_order="1", ope_name="TEXT", ope_text=u"文字",
                            operate_text=u"设置文字", check_text=u"设置文字", ope_desc=u"")),
    LibWidgetOperation(dict(id="40202", type_name="SELECT", ope_order="1", ope_name="LABEL", ope_text=u"标签",
                            operate_text=u"设置标签", check_text=u"检查标签", ope_desc=u"")),
    LibWidgetOperation(dict(id="40203", type_name="SELECT", ope_order="1", ope_name="VALUE", ope_text=u"值",
                            operate_text=u"设置值", check_text=u"检查值", ope_desc=u"")),

    LibWidgetOperation(dict(id="40301", type_name="INP", ope_order="1", ope_name="INPUT", ope_text=u"输入",
                            operate_text=u"输入", check_text=u"", ope_desc=u"")),

    LibWidgetOperation(dict(id="40401", type_name="ALERT", ope_order="1", ope_name="ACCEPT", ope_text=u"确定",
                            operate_text=u"确定", check_text=u"", ope_desc=u"")),
    LibWidgetOperation(dict(id="40402", type_name="ALERT", ope_order="2", ope_name="DISMISS", ope_text=u"取消",
                            operate_text=u"取消", check_text=u"", ope_desc=u""))]

from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import LibWidgetType
from OrcLib.LibDatabase import LibWidgetOperation

orc_db.session.query(LibDictionary).delete()
orc_db.session.query(LibWidgetType).delete()
orc_db.session.query(LibWidgetOperation).delete()

# orc_db.drop_all()
# orc_db.create_all()

orc_db.session.add_all(init_value_widget_type)
orc_db.session.add_all(init_value_widget_operation)
orc_db.session.add_all(init_value_dictionary)
# orc_db.session.add_all(init_value_sequence)


orc_db.session.commit()
