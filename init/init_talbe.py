# coding=utf-8
from OrcApi import orc_db

from OrcLib.LibDatabase import LibDictionary
from OrcLib.LibDatabase import LibSequence

from OrcLib.LibDatabase import LibWidgetType
from OrcLib.LibDatabase import LibWidgetOperation


dict_batch_type = [
    ('10101', 'batch_type', '1', 'BATCH_SUITE', u'计划组', '', u'用于存放批量计划'),
    ('10102', 'batch_type', '2', 'BATCH', u'计划', '', u'单个计划')]

dict_case_type = [
    ('10201', 'case_type', '1', 'CASE_SUITE', u'用例组', '', u'用于存放批量用例'),
    ('10202', 'case_type', '2', 'CASE', u'用例', '', u'单个用例'),
    ('10203', 'case_type', '3', 'FUNC_SUITE', u'函数组', '', u'函数组'),
    ('10204', 'case_type', '3', 'FUNC', u'函数', '', u'用例但不能单独执行')]

dict_item_type = [
    ('10301', 'step_type', '1', 'STEP_NORMAL', u'普通步骤', '', u'普通步骤'),
    ('10302', 'step_type', '1', 'STEP_FUNC', u'函数步骤', '', u'函数步骤'),
    ('10401', 'item_type', '1', 'WEB', 'WEB', '', ''),
    ('10402', 'item_type', '2','DATA', u'数据', '', ''),
    ('10403', 'item_type', '3', 'IOS', 'IOS', '', ''),
    ('10404', 'item_type', '4', 'ANDROID', 'ANDROID', '', ''),
    ('10405', 'item_type', '5', 'JSON', u'JSON接口', '', ''),
    ('10406', 'item_type', '6', 'WEBSERVICE', 'WEBSERVICE', '', ''),
    ('10501', 'item_mode', '1', 'OPERATE', u'操作项', '', u'执行操作'),
    ('10502', 'item_mode', '2', 'CHECK', u'检查项', '', u'执行检查')]

dict_data_mode = [
    ('10601', 'data_mode', '1', 'DEFAULT', u'默认', '', ''),
    ('10602', 'data_mode', '2', 'FILE', u'文件', '', ''),
    ('10603', 'data_mode', '3', 'DATABASE', u'数据库', '', '')]

dict_data_type = [
    ('10701', 'data_type', '1', 'INT', u'整数', '', ''),
    ('10702', 'data_type', '2', 'STR', u'字符', '', ''),
    ('10703', 'data_type', '3', 'ARRAY', u'数组', '', ''),
    ('10704', 'data_type', '4', 'USER_DEFINE', u'自定义', '', '')]

dict_widget_attr_type = [
    ('10801', 'widget_attr_type', '1', 'ID', 'ID', '', ''),
    ('10802', 'widget_attr_type', '2', 'NAME', 'NAME', '', ''),
    ('10803', 'widget_attr_type', '3', 'XPATH', 'XPATH', '', ''),
    ('10804', 'widget_attr_type', '4', 'TAGNAME', u'标签名称', '', ''),
    ('10805', 'widget_attr_type', '5', 'LINK_TEXT', u'链接文字', '', ''),
    ('10806', 'widget_attr_type', '6', 'CSS', 'CSS', '', ''),
    ('10807', 'widget_attr_type', '7', 'LAST_CHILD', u'最末子节点', '', '')]

dict_src_type = [
    ('10901', 'src_type', '1', 'BATCH', u'计划', '', ''),
    ('10902', 'src_type', '2', 'CASE', u'用例', '', ''),
    ('10903', 'src_type', '3', 'STEP', u'步骤', '', ''),
    ('10904', 'src_type', '4', 'ITEM', u'执行项', '', '')]

dict_operate_object_type = [
    ('11001', 'operate_object_type', '1', 'PAGE', u'页面', '(\'operation\',)', ''),
    ('11002', 'operate_object_type', '2', 'WINDOW', u'窗口', '', ''),
    ('11003', 'operate_object_type', '3', 'WIDGET', u'控件', '(\'operation\', \'check\')', '')]

dict_run_def = [
    ('11101', 'run_def', '3','TEST', u'执行记录', '', '')]

dict_test_env = [
    ('11201', 'test_env', '1', 'TEST', u'测试环境', '', ''),
    ('11202', 'test_env', '2', 'PRE', u'预生产环境', '', ''),
    ('11203', 'test_env', '3', 'PRD', u'生产环境', '', '')]

dict_browser = [
    ('11301', 'browser', '1', 'FIREFOX', 'FIREFOX', '', ''),
    ('11302', 'browser', '2', 'CHROME', 'CHROME', '', ''),
    ('11303', 'browser', '3', 'IE', 'IE', '', ''),
    ('11304', 'browser', '4', 'EDGE', 'EDGE', '', ''),
    ('11305', 'browser', '5', 'PHANTOMJS', 'PHANTOMJS', '', ''),
    ('11306', 'browser', '6', 'SAFARI', 'SAFARI', '', ''),
    ('11307', 'browser', '7', 'HTMLUNIT', 'HTMLUNIT', '', '')]

dict_data_src_type = [
    ('11401', 'data_src_type', '1', 'SQLite', 'SQLite', '', ''),
    ('11402', 'data_src_type', '2', 'MySql', 'MySql', '', ''),
    ('11403', 'data_src_type', '3', 'Oracle', 'Oracle', '', '')]

dict_result = [
    ('11501', 'result', '1', 'PASS', u'通过', '', ''),
    ('11502', 'result', '2', 'FAIL', u'失败', '', '')]

seq = (
    ('20001', 'batch_def', '100000000'),
    ('20002', 'batch_det', '110000000'),
    ('20003', 'case_def', '200000000'),
    ('20004', 'case_det', '210000000'),
    ('20005', 'step_def', '220000000'),
    ('20006', 'step_det', '230000000'),
    ('20007', 'item', '240000000'),
    ('20008', 'page_def', '300000000'),
    ('20009', 'page_det', '310000000'),
    ('20010', 'window_def', '320000000'),
    ('20011', 'widget_def', '330000000'),
    ('20012', 'widget_det', '340000000'),
    ('20013', 'data', '400000000'),
    ('20014', 'dictionary', '20000'),
    ('20015', 'widget_type', '21000'),
    ('20016', 'widget_operation', '22000'))

widget_type = (
    ('30001', 1, 'PRO', 'GROUP', u'控件组', ''),
    ('30004', 4, 'PRO', 'FRAME', u'FRAME', ''),
    ('30005', 5, 'PRO', 'BLOCK', u'块', ''),
    ('30006', 6, 'PRO', 'INP', u'输入框', ''),
    ('30007', 7, 'PRO', 'BTN', u'按钮', ''),
    ('30008', 8, 'PRO', 'LINK', u'链接', ''),
    ('30009', 9, 'PRO', 'SELECT', u'下拉框', ''),
    ('30010', 10, 'PRO', 'ALERT', u'提示框', ''),
    ('30011', 11, 'PRO', 'MULTI', u'多控件', ''))

widget_operation_page = (
    ('40001', 'PAGE', '1', 'GET', u'打开', u'打开', u'', u''),
    ('40002', 'PAGE', '2', 'MAX', u'最大化', u'最大化', u'', u''))

widget_operation_block = (
    ('40101', 'BLOCK', '1', 'EXISTS', u'存在', u'', u'检查存在', u''),
    ('40102', 'BLOCK', '2', 'CLICK', u'点击', u'点击', u'', u''),
    ('40103', 'BLOCK', '3', 'GET_ATTR', u'获取属性', u'', u'检查属性', u''),
    ('40104', 'BLOCK', '4', 'GET_TEXT', u'获取文本', u'', u'检查文本', u''),
    ('40105', 'BLOCK', '5', 'GET_HTML', u'获取HTML', u'', u'', u''),
    ('40106', 'BLOCK', '6', 'SET_ATTR', u'设置属性', u'设置属性', u'', u''),
    ('40107', 'BLOCK', '7', 'DEL_ATTR', u'删除属性', u'删除属性', u'', u''),
    ('40108', 'BLOCK', '8', 'SCROLL', u'滚动至显示', u'滚动至显示', u'', u''),
    ('40109', 'BLOCK', '9', 'FOCUS', u'焦点至', u'焦点至', u'', u''),
    ('40110', 'BLOCK', '10', 'SCRIPT', u'运行脚本', u'运行脚本', u'', u''))

widget_operation_select = (
    ('40201', 'SELECT', '1', 'TEXT', u'文字', u'设置文字', u'检查文字', u''),
    ('40202', 'SELECT', '1', 'LABEL', u'标签', u'设置标签', u'检查标签', u''),
    ('40203', 'SELECT', '1', 'VALUE', u'值', u'设置值', u'检查值', u''))

widget_operation_inp = (
    ('40301', 'INP', '1', 'INPUT', u'输入', u'输入', u'', u''),)

widget_operation_alert = (
    ('40401', 'ALERT', '1', 'ACCEPT', u'确定', u'确定', u'', u''),
    ('40402', 'ALERT', '2', 'DISMISS', u'取消', u'取消', u'', u''))

widget_operation_multi = (
    ('40501', 'MULTI', '1', 'DRAG_AND_DROP', u'拖放', u'拖放', u'', u''),)

init_value_dictionary = []
for _file in (dict_batch_type, dict_case_type, dict_item_type, dict_data_mode, dict_data_type,
              dict_widget_attr_type, dict_src_type, dict_operate_object_type, dict_run_def,
              dict_test_env, dict_browser, dict_data_src_type, dict_result):
    for _item in _file:
        init_value_dictionary.append(LibDictionary(dict(
            id=_item[0],
            dict_flag=_item[1],
            dict_order=_item[2],
            dict_value=_item[3],
            dict_text=_item[4],
            dict_param=_item[5],
            dict_desc=_item[6])))

init_value_sequence = []
for _item in seq:
    init_value_sequence.append(LibSequence(dict(id=_item[0], field_name=_item[1], field_seq=_item[2])))

init_value_widget_type = []
for _item in widget_type:
    init_value_widget_type.append(LibWidgetType(dict(
        id=_item[0],
        type_order=_item[1],
        type_mode=_item[2],
        type_name=_item[3],
        type_text=_item[4],
        type_desc=_item[5])))

init_value_widget_operation = []
for _file in (widget_operation_page, widget_operation_block, widget_operation_multi,
              widget_operation_select, widget_operation_inp, widget_operation_alert):
    for _item in _file:
        init_value_widget_operation.append(LibWidgetOperation(dict(
            id=_item[0],
            type_name=_item[1],
            ope_order=_item[2],
            ope_name=_item[3],
            ope_text=_item[4],
            operate_text=_item[5],
            check_text=_item[6],
            ope_desc=_item[7])))

orc_db.session.query(LibDictionary).delete()
orc_db.session.query(LibSequence).delete()
orc_db.session.query(LibWidgetType).delete()
orc_db.session.query(LibWidgetOperation).delete()

# orc_db.drop_all()
# orc_db.create_all()

orc_db.session.add_all(init_value_widget_type)
orc_db.session.add_all(init_value_widget_operation)
orc_db.session.add_all(init_value_dictionary)
orc_db.session.add_all(init_value_sequence)

orc_db.session.commit()
