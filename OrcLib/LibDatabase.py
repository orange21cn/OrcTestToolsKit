# -*- coding: utf-8 -*-
from datetime import datetime

from OrcLib.LibCommon import OrcCover
from OrcApi import orc_db


def gen_id(p_name):
    _seq = orc_db.session \
        .query(LibSequence) \
        .filter(LibSequence.field_name == p_name) \
        .first()
    _seq.field_seq += 1
    orc_db.session.commit()

    return _seq.field_seq


class TabBatchDef(orc_db.Model):
    """
    Table orc_batch_def
    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    pid = orc_db.Column(orc_db.Integer)
    batch_no = orc_db.Column(orc_db.String(16))
    batch_name = orc_db.Column(orc_db.String(32))
    batch_desc = orc_db.Column(orc_db.String(512))
    comment = orc_db.Column(orc_db.String(1024))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):

        if p_def is not None:

            self.id = p_def["id"]
            self.pid = p_def["pid"]
            self.batch_no = p_def["batch_no"]
            self.batch_name = p_def["batch_name"]
            self.batch_desc = p_def["batch_desc"]
            self.comment = p_def["comment"]
            self.create_time = OrcCover.str2time(p_def["create_time"])
            self.modify_time = OrcCover.str2time(p_def["modify_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            pid=str(self.pid),
            batch_no=self.batch_no,
            batch_name=self.batch_name,
            batch_desc=self.batch_desc,
            comment=self.comment,
            create_time=OrcCover.time2str(self.create_time),
            modify_time=OrcCover.time2str(self.modify_time)
        )


class TabBatchDet(orc_db.Model):
    """
    Table tab_batch_det
    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    batch_id = orc_db.Column(orc_db.Integer)
    case_id = orc_db.Column(orc_db.Integer)
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):

        if p_def is not None:

            self.id = p_def["id"]
            self.batch_id = p_def["batch_id"]
            self.case_id = p_def["case_id"]
            self.create_time = OrcCover.str2time(p_def["create_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            batch_id=str(self.batch_id),
            case_id=str(self.case_id),
            create_time=OrcCover.time2str(self.create_time)
        )


class TabCaseDef(orc_db.Model):
    """
    Table tab_case_def
    """
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

        if p_def is not None:

            self.id = p_def["id"]
            self.pid = p_def["pid"]
            self.case_no = p_def["case_no"]
            self.case_path = p_def["case_path"]
            self.case_type = p_def["case_type"]
            self.case_name = p_def["case_name"]
            self.case_desc = p_def["case_desc"]
            self.comment = p_def["comment"]
            self.create_time = OrcCover.str2time(p_def["create_time"])
            self.modify_time = OrcCover.str2time(p_def["modify_time"])

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
            create_time=OrcCover.time2str(self.create_time),
            modify_time=OrcCover.time2str(self.modify_time)
        )


class TabCaseDet(orc_db.Model):
    """
    Table tab_case_det
    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    case_id = orc_db.Column(orc_db.Integer)
    step_id = orc_db.Column(orc_db.Integer)
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):

        if p_def is not None:

            self.id = p_def["id"]
            self.case_id = p_def["case_id"]
            self.step_id = p_def["step_id"]
            self.create_time = OrcCover.str2time(p_def["create_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            case_id=str(self.case_id),
            step_id=str(self.step_id),
            create_time=OrcCover.time2str(self.create_time)
        )


class TabStepDef(orc_db.Model):
    """
    Table tab_step_def
    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    step_no = orc_db.Column(orc_db.String(8))
    step_desc = orc_db.Column(orc_db.String(512))
    comment = orc_db.Column(orc_db.String(1024))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):

        if p_def is not None:

            self.id = p_def["id"]
            self.step_no = p_def["step_no"]
            self.step_desc = p_def["step_desc"]
            self.comment = p_def["comment"]
            self.create_time = OrcCover.str2time(p_def["create_time"])
            self.modify_time = OrcCover.str2time(p_def["modify_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            step_no=self.step_no,
            step_desc=self.step_desc,
            comment=self.comment,
            create_time=OrcCover.time2str(self.create_time),
            modify_time=OrcCover.time2str(self.modify_time)
        )


class TabStepDet(orc_db.Model):
    """

    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    step_id = orc_db.Column(orc_db.Integer)
    item_id = orc_db.Column(orc_db.Integer)
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):

        if p_def is not None:

            self.id = p_def["id"]
            self.step_id = p_def["step_id"]
            self.item_id = p_def["item_id"]
            self.create_time = OrcCover.str2time(p_def["create_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            step_id=str(self.step_id),
            item_id=str(self.item_id),
            create_time=OrcCover.time2str(self.create_time)
        )


class TabItem(orc_db.Model):
    """

    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    item_no = orc_db.Column(orc_db.String(32))
    item_type = orc_db.Column(orc_db.String(8))
    item_mode = orc_db.Column(orc_db.String(8))
    item_operate = orc_db.Column(orc_db.String(256))
    item_desc = orc_db.Column(orc_db.String(256))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):

        if p_def is not None:

            self.id = p_def["id"]
            self.item_no = p_def["item_no"]
            self.item_type = p_def["item_type"]
            self.item_mode = p_def["item_mode"]
            self.item_operate = p_def["item_operate"]
            self.item_desc = p_def["item_desc"]
            self.comment = p_def["comment"]
            self.create_time = OrcCover.str2time(p_def["create_time"])
            self.modify_time = OrcCover.str2time(p_def["modify_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            item_no=self.item_no,
            item_type=self.item_type,
            item_mode=self.item_mode,
            item_operate=self.item_operate,
            item_desc=self.item_desc,
            comment=self.comment,
            create_time=OrcCover.time2str(self.create_time),
            modify_time=OrcCover.time2str(self.modify_time)
        )


class TabData(orc_db.Model):
    """
    Data table
    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    src_id = orc_db.Column(orc_db.Integer)
    src_type = orc_db.Column(orc_db.String(16))
    data_flag = orc_db.Column(orc_db.String(32))
    data_order = orc_db.Column(orc_db.Integer)
    data_type = orc_db.Column(orc_db.String(16))
    data_mode = orc_db.Column(orc_db.String(16))
    data_value = orc_db.Column(orc_db.String(128))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):
        if p_def is not None:

            self.id = p_def["id"]
            self.src_id = p_def["src_id"]
            self.src_type = p_def["src_type"]
            self.data_flag = p_def["data_flag"]
            self.data_order = p_def["data_order"]
            self.data_type = p_def["data_type"]
            self.data_mode = p_def["data_mode"]
            self.data_value = p_def["data_value"]
            self.comment = p_def["comment"]
            self.create_time = OrcCover.str2time(p_def["create_time"])
            self.modify_time = OrcCover.str2time(p_def["modify_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            src_id=str(self.src_id),
            src_type=self.src_type,
            data_flag=self.data_flag,
            data_order=str(self.data_order),
            data_type=self.data_type,
            data_mode=self.data_mode,
            data_value=self.data_value,
            comment=self.comment,
            create_time=OrcCover.time2str(self.create_time),
            modify_time=OrcCover.time2str(self.modify_time)
        )


class WebPageDef(orc_db.Model):
    """
    Table page definition
    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    page_flag = orc_db.Column(orc_db.String(32))
    page_desc = orc_db.Column(orc_db.String(32))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):

        if p_def is not None:

            self.id = p_def["id"]
            self.page_flag = p_def["page_flag"]
            self.page_desc = p_def["page_desc"]
            self.comment = p_def["comment"]
            self.create_time = OrcCover.str2time(p_def["create_time"])
            self.modify_time = OrcCover.str2time(p_def["modify_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            page_flag=self.page_flag,
            page_desc=self.page_desc,
            comment=self.comment,
            create_time=OrcCover.time2str(self.create_time),
            modify_time=OrcCover.time2str(self.modify_time)
        )


class WebPageDet(orc_db.Model):
    """
    Table page detail
    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    page_id = orc_db.Column(orc_db.Integer, primary_key=True)
    page_env = orc_db.Column(orc_db.String(32))
    page_url = orc_db.Column(orc_db.String(32))
    comment = orc_db.Column(orc_db.String(512))
    create_time = orc_db.Column(orc_db.DateTime, default=datetime.now())
    modify_time = orc_db.Column(orc_db.DateTime, default=datetime.now())

    def __init__(self, p_def=None):

        if p_def is not None:

            self.id = p_def["id"]
            self.page_id = p_def["page_id"]
            self.page_env = p_def["page_env"]
            self.page_url = p_def["page_url"]
            self.comment = p_def["comment"]
            self.create_time = OrcCover.str2time(p_def["create_time"])
            self.modify_time = OrcCover.str2time(p_def["modify_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            page_id=str(self.page_id),
            page_env=self.page_env,
            page_url=self.page_url,
            comment=self.comment,
            create_time=OrcCover.time2str(self.create_time),
            modify_time=OrcCover.time2str(self.modify_time)
        )


class WebWidgetDef(orc_db.Model):
    """
    Table widget definition
    """
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

        if p_def is not None:

            self.id = p_def["id"]
            self.pid = p_def["pid"]
            self.widget_flag = p_def["widget_flag"]
            self.widget_path = p_def["widget_path"]
            self.widget_type = p_def["widget_type"]
            self.widget_desc = p_def["widget_desc"]
            self.comment = p_def["comment"]
            self.create_time = OrcCover.str2time(p_def["create_time"])
            self.modify_time = OrcCover.str2time(p_def["modify_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            pid=str(self.pid),
            widget_flag=self.widget_flag,
            widget_path=self.widget_path,
            widget_type=self.widget_type,
            widget_desc=self.widget_desc,
            comment=self.comment,
            create_time=OrcCover.time2str(self.create_time),
            modify_time=OrcCover.time2str(self.modify_time)
        )


class WebWidgetDet(orc_db.Model):
    """
    Table widget definition
    """
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

        if p_def is not None:

            self.id = p_def["id"]
            self.widget_id = p_def["widget_id"]
            self.widget_order = p_def["widget_order"]
            self.widget_attr_type = p_def["widget_attr_type"]
            self.widget_attr_value = p_def["widget_attr_value"]
            self.widget_desc = p_def["widget_desc"]
            self.comment = p_def["comment"]
            self.create_time = OrcCover.str2time(p_def["create_time"])
            self.modify_time = OrcCover.str2time(p_def["modify_time"])

    def to_json(self):

        return dict(
            id=str(self.id),
            widget_id=self.widget_id,
            widget_order=self.widget_order,
            widget_attr_type=self.widget_attr_type,
            widget_attr_value=self.widget_attr_value,
            widget_desc=self.widget_desc,
            comment=self.comment,
            create_time=OrcCover.time2str(self.create_time),
            modify_time=OrcCover.time2str(self.modify_time)
        )


class LibDictionary(orc_db.Model):
    """
    Table dictionary
    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    dict_flag = orc_db.Column(orc_db.String(32))
    dict_order = orc_db.Column(orc_db.String(32))
    dict_value = orc_db.Column(orc_db.String(16))
    dict_text = orc_db.Column(orc_db.String(16))
    dict_desc = orc_db.Column(orc_db.String(255))

    def __init__(self, p_data):
        """
        :param p_data: dict
        :return: None
        """
        if "id" in p_data:
            self.id = p_data["id"]
        elif "" in p_data:
            self.dict_flag = p_data["dict_flag"]
        elif "dict_flag" in p_data:
            self.dict_order = p_data["dict_order"]
        elif "dict_value" in p_data:
            self.dict_value = p_data["dict_value"]
        elif "dict_text" in p_data:
            self.dict_text = p_data["dict_text"]
        elif "dict_desc" in p_data:
            self.dict_desc = p_data["dict_desc"]
        else:
            pass

    def to_json(self):
        _value = {
            "id": str(self.id),
            "dict_flag": self.dict_flag,
            "dict_order": self.dict_order,
            "dict_value": self.dict_value,
            "dict_text": self.dict_text,
            "dict_desc": self.dict_desc
        }
        return _value


class LibSequence(orc_db.Model):
    """
    Table sequence
    """
    id = orc_db.Column(orc_db.Integer, primary_key=True)
    field_name = orc_db.Column(orc_db.String(32))
    field_seq = orc_db.Column(orc_db.Integer)

    def __init__(self):
        pass
