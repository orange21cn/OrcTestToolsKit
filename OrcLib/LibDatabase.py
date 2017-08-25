# -*- coding: utf-8 -*-
from datetime import datetime
from OrcLib.LibCommon import OrcCovert
from OrcLib.LibProgram import OrcFactory
from OrcApi import orc_db


def gen_id(p_name):
    """
    生成 id
    :param p_name:
    :return: id
    """
    sequence = orc_db.session \
        .query(LibSequence) \
        .filter(LibSequence.field_name == p_name) \
        .first()

    sequence.field_seq += 1
    orc_db.session.commit()

    return sequence.field_seq


class TabRunTime(orc_db.Model):
    """
    Table tab_run_time
    """
    __tablename__ = 'tab_run_time'

    id = orc_db.Column(orc_db.Integer, autoincrement=True, primary_key=True)
    module = orc_db.Column(orc_db.String(16))
    data_flag = orc_db.Column(orc_db.String(16))
    data_index = orc_db.Column(orc_db.Integer)
    data_value = orc_db.Column(orc_db.String(128))

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.module = data.value('module')
        self.data_flag = data.value('data_flag')
        self.data_index = data.value('data_flag')
        self.data_value = data.value('data_flag')

    def to_json(self):

        return dict(
            id=self.id,
            module=self.module,
            data_flag=self.data_flag,
            data_index=self.data_index,
            data_value=self.data_value
        )


class TabBatchDef(orc_db.Model):
    """
    Table orc_batch_def
    """
    __tablename__ = 'tab_batch_def'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    pid = orc_db.Column(orc_db.Integer)
    batch_no = orc_db.Column(orc_db.String(16))
    batch_type = orc_db.Column(orc_db.String(8))
    batch_name = orc_db.Column(orc_db.String(32))
    batch_desc = orc_db.Column(orc_db.String(512))
    comment = orc_db.Column(orc_db.String(1024))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.pid = data.value('pid')
        self.batch_no = data.value('batch_no')
        self.batch_type = data.value('batch_type')
        self.batch_name = data.value('batch_name')
        self.batch_desc = data.value('batch_desc')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            pid=self.pid,
            batch_no=self.batch_no,
            batch_type=self.batch_type,
            batch_name=self.batch_name,
            batch_desc=self.batch_desc,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class TabBatchDet(orc_db.Model):
    """
    Table tab_batch_det
    """
    __tablename__ = 'tab_batch_det'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    batch_id = orc_db.Column(orc_db.Integer)
    case_id = orc_db.Column(orc_db.Integer)
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.batch_id = data.value('batch_id')
        self.case_id = data.value('case_id')
        self.create_time = OrcCovert.str2time(data.value('create_time'))

    def to_json(self):

        return dict(
            id=self.id,
            batch_id=self.batch_id,
            case_id=self.case_id,
            create_time=OrcCovert.time2str(self.create_time)
        )


class TabCaseDef(orc_db.Model):
    """
    Table tab_case_def
    """
    __tablename__ = 'tab_case_def'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    pid = orc_db.Column(orc_db.Integer)
    case_no = orc_db.Column(orc_db.String(8))
    case_path = orc_db.Column(orc_db.String(32))
    case_type = orc_db.Column(orc_db.String(8))
    case_name = orc_db.Column(orc_db.String(64))
    case_desc = orc_db.Column(orc_db.String(512))
    comment = orc_db.Column(orc_db.String(1024))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.pid = data.value('pid')
        self.case_no = data.value('case_no')
        self.case_path = data.value('case_path')
        self.case_type = data.value('case_type')
        self.case_name = data.value('case_name')
        self.case_desc = data.value('case_desc')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            pid=self.pid,
            case_no=self.case_no,
            case_path=self.case_path,
            case_type=self.case_type,
            case_name=self.case_name,
            case_desc=self.case_desc,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class TabCaseDet(orc_db.Model):
    """
    Table tab_case_det
    """
    __tablename__ = 'tab_case_det'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    case_id = orc_db.Column(orc_db.Integer)
    step_id = orc_db.Column(orc_db.Integer)
    step_no = orc_db.Column(orc_db.String(8))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.case_id = data.value('case_id')
        self.step_id = data.value('step_id')
        self.step_no = data.value('step_no')
        self.create_time = OrcCovert.str2time(data.value('create_time'))

    def to_json(self):

        return dict(
            id=self.id,
            case_id=self.case_id,
            step_id=self.step_id,
            step_no=self.step_no,
            create_time=OrcCovert.time2str(self.create_time)
        )


class TabStepDef(orc_db.Model):
    """
    Table tab_step_def
    """
    __tablename__ = 'tab_step_def'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    step_type = orc_db.Column(orc_db.String(8))
    step_desc = orc_db.Column(orc_db.String(512))
    comment = orc_db.Column(orc_db.String(1024))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)
        
        self.id = data.value('id')
        self.step_type = data.value('step_type')
        self.step_desc = data.value('step_desc')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            step_type=self.step_type,
            step_desc=self.step_desc,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class TabStepDet(orc_db.Model):
    """

    """
    __tablename__ = 'tab_step_det'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    step_id = orc_db.Column(orc_db.Integer)
    item_id = orc_db.Column(orc_db.Integer)
    item_no = orc_db.Column(orc_db.String(32))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.step_id = data.value('step_id')
        self.item_id = data.value('item_id')
        self.item_no = data.value('item_no')
        self.create_time = OrcCovert.str2time(data.value('create_time'))

    def to_json(self):

        return dict(
            id=self.id,
            step_id=self.step_id,
            item_id=self.item_id,
            item_no=self.item_no,
            create_time=OrcCovert.time2str(self.create_time)
        )


class TabItem(orc_db.Model):
    """

    """
    __tablename__ = 'tab_item'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    item_type = orc_db.Column(orc_db.String(8))
    item_mode = orc_db.Column(orc_db.String(8))
    item_operate = orc_db.Column(orc_db.String(256))
    item_desc = orc_db.Column(orc_db.String(256))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.item_type = data.value('item_type')
        self.item_mode = data.value('item_mode')
        self.item_operate = data.value('item_operate')
        self.item_desc = data.value('item_desc')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            item_type=self.item_type,
            item_mode=self.item_mode,
            item_operate=self.item_operate,
            item_desc=self.item_desc,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class TabData(orc_db.Model):
    """
    Data table
    """
    __tablename__ = 'tab_data'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    test_env = orc_db.Column(orc_db.String(16))
    src_id = orc_db.Column(orc_db.Integer)
    src_type = orc_db.Column(orc_db.String(16))
    step_order = orc_db.Column(orc_db.Integer)
    data_flag = orc_db.Column(orc_db.String(32))
    data_order = orc_db.Column(orc_db.Integer)
    data_type = orc_db.Column(orc_db.String(16))
    data_mode = orc_db.Column(orc_db.String(16))
    data_value = orc_db.Column(orc_db.String(128))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.test_env = data.value('test_env')
        self.src_id = data.value('src_id')
        self.src_type = data.value('src_type')
        self.step_order = data.value('step_order')
        self.data_flag = data.value('data_flag')
        self.data_order = data.value('data_order')
        self.data_type = data.value('data_type')
        self.data_mode = data.value('data_mode')
        self.data_value = data.value('data_value')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            test_env=self.test_env,
            src_id=self.src_id,
            src_type=self.src_type,
            step_order=self.step_order,
            data_flag=self.data_flag,
            data_order=self.data_order,
            data_type=self.data_type,
            data_mode=self.data_mode,
            data_value=self.data_value,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class WebPageDef(orc_db.Model):
    """
    Table page definition
    """
    __tablename__ = 'web_page_def'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    page_flag = orc_db.Column(orc_db.String(32))
    page_desc = orc_db.Column(orc_db.String(32))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.page_flag = data.value('page_flag')
        self.page_desc = data.value('page_desc')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            page_flag=self.page_flag,
            page_desc=self.page_desc,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class WebPageDet(orc_db.Model):
    """
    Table page detail
    """
    __tablename__ = 'web_page_det'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    page_id = orc_db.Column(orc_db.Integer, primary_key=True)
    test_env = orc_db.Column(orc_db.String(32))
    page_url = orc_db.Column(orc_db.String(512))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.page_id = data.value('page_id')
        self.test_env = data.value('test_env')
        self.page_url = data.value('page_url')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            page_id=self.page_id,
            test_env=self.test_env,
            page_url=self.page_url,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class WebWidgetDef(orc_db.Model):
    """
    Table widget definition
    """
    __tablename__ = 'web_widget_def'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    pid = orc_db.Column(orc_db.Integer)
    widget_flag = orc_db.Column(orc_db.String(8))
    widget_path = orc_db.Column(orc_db.String(32))
    widget_type = orc_db.Column(orc_db.String(16))
    widget_desc = orc_db.Column(orc_db.String(255))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.pid = data.value('pid')
        self.widget_flag = data.value('widget_flag')
        self.widget_path = data.value('widget_path')
        self.widget_type = data.value('widget_type')
        self.widget_desc = data.value('widget_desc')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            pid=self.pid,
            widget_flag=self.widget_flag,
            widget_path=self.widget_path,
            widget_type=self.widget_type,
            widget_desc=self.widget_desc,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class WebWidgetDet(orc_db.Model):
    """
    Table widget definition
    """
    __tablename__ = 'web_widget_det'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    widget_id = orc_db.Column(orc_db.Integer)
    widget_order = orc_db.Column(orc_db.String(16))
    widget_attr_type = orc_db.Column(orc_db.String(16))
    widget_attr_value = orc_db.Column(orc_db.String(64))
    widget_desc = orc_db.Column(orc_db.String(255))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.widget_id = data.value('widget_id')
        self.widget_order = data.value('widget_order')
        self.widget_attr_type = data.value('widget_attr_type')
        self.widget_attr_value = data.value('widget_attr_value')
        self.widget_desc = data.value('widget_desc')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            widget_id=self.widget_id,
            widget_order=self.widget_order,
            widget_attr_type=self.widget_attr_type,
            widget_attr_value=self.widget_attr_value,
            widget_desc=self.widget_desc,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class WebWindowDef(orc_db.Model):
    """
    Table widget definition
    """
    __tablename__ = 'web_window_def'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    window_mark = orc_db.Column(orc_db.String(16))
    window_desc = orc_db.Column(orc_db.String(255))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.window_mark = data.value('window_mark')
        self.window_desc = data.value('window_desc')
        self.comment = data.value('comment')
        self.create_time = OrcCovert.str2time(data.value('create_time'))
        self.modify_time = OrcCovert.str2time(data.value('modify_time'))

    def to_json(self):

        return dict(
            id=self.id,
            window_mark=self.window_mark,
            window_desc=self.window_desc,
            comment=self.comment,
            create_time=OrcCovert.time2str(self.create_time),
            modify_time=OrcCovert.time2str(self.modify_time)
        )


class LibDictionary(orc_db.Model):
    """
    Table dictionary
    """
    __tablename__ = 'lib_dictionary'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    dict_flag = orc_db.Column(orc_db.String(32))
    dict_order = orc_db.Column(orc_db.String(32))
    dict_value = orc_db.Column(orc_db.String(16))
    dict_text = orc_db.Column(orc_db.String(16))
    dict_param = orc_db.Column(orc_db.String(128))
    dict_desc = orc_db.Column(orc_db.String(255))

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.dict_flag = data.value('dict_flag')
        self.dict_order = data.value('dict_order')
        self.dict_value = data.value('dict_value')
        self.dict_text = data.value('dict_text')
        self.dict_param = data.value('dict_param')
        self.dict_desc = data.value('dict_desc')

    def to_json(self):

        return dict(
            id=self.id,
            dict_flag=self.dict_flag,
            dict_order=self.dict_order,
            dict_value=self.dict_value,
            dict_text=self.dict_text,
            dict_param=self.dict_param,
            dict_desc=self.dict_desc
        )


class LibWidgetType(orc_db.Model):
    """
    Table dictionary
    """
    __tablename__ = 'lib_widget_type'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    type_order = orc_db.Column(orc_db.Integer)
    type_mode = orc_db.Column(orc_db.String(16))  # 固有或自定义
    type_name = orc_db.Column(orc_db.String(16), unique=True)
    type_text = orc_db.Column(orc_db.String(16))
    type_desc = orc_db.Column(orc_db.String(255))

    def __init__(self, p_def):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.type_order = data.value('type_order')
        self.type_mode = data.value('type_mode')
        self.type_name = data.value('type_name')
        self.type_text = data.value('type_text')
        self.type_desc = data.value('type_desc')

    def to_json(self):

        return dict(
            id=self.id,
            type_order=self.type_order,
            type_mode=self.type_mode,
            type_name=self.type_name,
            type_text=self.type_text,
            type_desc=self.type_desc
        )


class LibWidgetOperation(orc_db.Model):
    """
    Table dictionary
    """
    __tablename__ = 'lib_widget_operation'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    type_name = orc_db.Column(orc_db.String(16))
    ope_order = orc_db.Column(orc_db.Integer)
    ope_name = orc_db.Column(orc_db.String(16))
    ope_text = orc_db.Column(orc_db.String(16))
    operate_text = orc_db.Column(orc_db.String(16))
    check_text = orc_db.Column(orc_db.String(16))
    ope_desc = orc_db.Column(orc_db.String(255))

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.type_name = data.value('type_name')
        self.ope_order = data.value('ope_order')
        self.ope_name = data.value('ope_name')
        self.ope_text = data.value('ope_text')
        self.operate_text = data.value('operate_text')
        self.check_text = data.value('check_text')
        self.ope_desc = data.value('ope_desc')

    def to_json(self):

        return dict(
            id=self.id,
            type_name=self.type_name,
            ope_order=self.ope_order,
            ope_name=self.ope_name,
            ope_text=self.ope_text,
            operate_text=self.operate_text,
            check_text=self.check_text,
            ope_desc=self.ope_desc
        )


class LibSequence(orc_db.Model):
    """
    Table sequence
    """
    __tablename__ = 'lib_sequence'

    id = orc_db.Column(orc_db.Integer, primary_key=True)
    field_name = orc_db.Column(orc_db.String(32))
    field_seq = orc_db.Column(orc_db.Integer)

    def __init__(self, p_def=None):
        
        data = OrcFactory.create_default_dict(p_def)

        self.id = data.value('id')
        self.field_name = data.value('field_name')
        self.field_seq = data.value('field_seq')
