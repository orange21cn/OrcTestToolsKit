# -*- coding: utf-8 -*-
from datetime import datetime
from OrcLib.LibCommon import OrcCovert
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

        self.id = p_def["id"] if p_def else None
        self.module = p_def["module"] if p_def else None
        self.data_flag = p_def["data_flag"] if p_def else None
        self.data_index = p_def["data_flag"] if p_def else None
        self.data_value = p_def["data_flag"] if p_def else None

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

        self.id = p_def["id"] if p_def else None
        self.pid = p_def["pid"] if p_def else None
        self.batch_no = p_def["batch_no"] if p_def else None
        self.batch_type = p_def["batch_type"] if p_def else None
        self.batch_name = p_def["batch_name"] if p_def else None
        self.batch_desc = p_def["batch_desc"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
            pid=str(self.pid),
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

        self.id = p_def["id"] if p_def else None
        self.batch_id = p_def["batch_id"] if p_def else None
        self.case_id = p_def["case_id"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
            batch_id=str(self.batch_id),
            case_id=str(self.case_id),
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

        self.id = p_def["id"] if p_def else None
        self.pid = p_def["pid"] if p_def else None
        self.case_no = p_def["case_no"] if p_def else None
        self.case_path = p_def["case_path"] if p_def else None
        self.case_type = p_def["case_type"] if p_def else None
        self.case_name = p_def["case_name"] if p_def else None
        self.case_desc = p_def["case_desc"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
            pid=str(self.pid),
            case_no=str(self.case_no),
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

        self.id = p_def["id"] if p_def else None
        self.case_id = p_def["case_id"] if p_def else None
        self.step_id = p_def["step_id"] if p_def else None
        self.step_no = p_def["step_no"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
            case_id=str(self.case_id),
            step_id=str(self.step_id),
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
        self.id = p_def["id"] if p_def else None
        self.step_type = p_def["step_type"] if p_def else None
        self.step_desc = p_def["step_desc"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
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

        self.id = p_def["id"] if p_def else None
        self.step_id = p_def["step_id"] if p_def else None
        self.item_id = p_def["item_id"] if p_def else None
        self.item_no = p_def["item_no"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
            step_id=str(self.step_id),
            item_id=str(self.item_id),
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

        self.id = p_def["id"] if p_def else None
        self.item_type = p_def["item_type"] if p_def else None
        self.item_mode = p_def["item_mode"] if p_def else None
        self.item_operate = p_def["item_operate"] if p_def else None
        self.item_desc = p_def["item_desc"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
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

        self.id = p_def["id"] if p_def else None
        self.test_env = p_def["test_env"] if p_def else None
        self.src_id = p_def["src_id"] if p_def else None
        self.src_type = p_def["src_type"] if p_def else None
        self.step_order = p_def["step_order"] if p_def else None
        self.data_flag = p_def["data_flag"] if p_def else None
        self.data_order = p_def["data_order"] if p_def else None
        self.data_type = p_def["data_type"] if p_def else None
        self.data_mode = p_def["data_mode"] if p_def else None
        self.data_value = p_def["data_value"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
            test_env=self.test_env,
            src_id=str(self.src_id),
            src_type=self.src_type,
            step_order=self.step_order,
            data_flag=self.data_flag,
            data_order=str(self.data_order),
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

        self.id = p_def["id"] if p_def else None
        self.page_flag = p_def["page_flag"] if p_def else None
        self.page_desc = p_def["page_desc"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
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

        self.id = p_def["id"] if p_def else None
        self.page_id = p_def["page_id"] if p_def else None
        self.test_env = p_def["test_env"] if p_def else None
        self.page_url = p_def["page_url"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
            page_id=str(self.page_id),
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

        self.id = p_def["id"] if p_def else None
        self.pid = p_def["pid"] if p_def else None
        self.widget_flag = p_def["widget_flag"] if p_def else None
        self.widget_path = p_def["widget_path"] if p_def else None
        self.widget_type = p_def["widget_type"] if p_def else None
        self.widget_desc = p_def["widget_desc"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
            pid=str(self.pid),
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

        self.id = p_def["id"] if p_def else None
        self.widget_id = p_def["widget_id"] if p_def else None
        self.widget_order = p_def["widget_order"] if p_def else None
        self.widget_attr_type = p_def["widget_attr_type"] if p_def else None
        self.widget_attr_value = p_def["widget_attr_value"] if p_def else None
        self.widget_desc = p_def["widget_desc"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
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

        self.id = p_def["id"] if p_def else None
        self.window_mark = p_def["window_mark"] if p_def else None
        self.window_desc = p_def["window_desc"] if p_def else None
        self.comment = p_def["comment"] if p_def else None
        self.create_time = OrcCovert.str2time(p_def["create_time"]) if p_def else None
        self.modify_time = OrcCovert.str2time(p_def["modify_time"]) if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
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
        """
        :param p_def: dict
        :return: None
        """
        self.id = int(p_def["id"]) if p_def else None
        self.dict_flag = p_def["dict_flag"] if p_def else None
        self.dict_order = p_def["dict_order"] if p_def else None
        self.dict_value = p_def["dict_value"] if p_def else None
        self.dict_text = p_def["dict_text"] if p_def else None
        self.dict_param = p_def["dict_param"] if p_def else None
        self.dict_desc = p_def["dict_desc"] if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
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

        self.id = int(p_def["id"]) if p_def else None
        self.type_order = p_def["type_order"] if p_def else None
        self.type_mode = p_def["type_mode"] if p_def else None
        self.type_name = p_def["type_name"] if p_def else None
        self.type_text = p_def["type_text"] if p_def else None
        self.type_desc = p_def["type_desc"] if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
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

        self.id = int(p_def["id"]) if p_def else None
        self.type_name = p_def["type_name"] if p_def else None
        self.ope_order = int(p_def["ope_order"]) if p_def else None
        self.ope_name = p_def["ope_name"] if p_def else None
        self.ope_text = p_def["ope_text"] if p_def else None
        self.operate_text = p_def["operate_text"] if p_def else None
        self.check_text = p_def["check_text"] if p_def else None
        self.ope_desc = p_def["ope_desc"] if p_def else None

    def to_json(self):

        return dict(
            id=str(self.id),
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

        self.id = int(p_def["id"]) if p_def else None
        self.field_name = p_def["field_name"] if p_def else None
        self.field_seq = p_def["field_seq"] if p_def else None
