# -*- coding: utf-8 -*-
# from app import app
# from app import orc_db
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sys
from PySide.QtGui import QApplication
from OrcView.StartView import StartView
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibTree import ModelTree
from PySide.QtGui import QStyledItemDelegate
from PySide.QtGui import QLabel
from PySide.QtCore import Qt

# from app import app
#
# app.run()

# from Data.models import OrcBatchDef
#
# ccc = OrcBatchDef()
# print ccc.get()

# User interface
import sys
from OrcView.Batch.BatchDef import ViewBatchDefMag
from OrcView.Lib.LibAdd import ViewAdd
from OrcView.StartView import StartView

reload(sys)
sys.setdefaultencoding('utf-8')

OrcData = QApplication(sys.argv)
_table_def = [{
        "ID": "id", "NAME": u"ID", "TYPE": "TEXT", "LENGTH": "16",
        "DISPLAY": "FALSE", "EDIT": "FALSE",
        "SEARCH": "FALSE", "ADD": "FALSE", "ESSENTIAL": "FALSE"
    }, {
        "ID": "pid", "NAME": u"父ID", "TYPE": "TEXT", "LENGTH": "16",
        "DISPLAY": "FALSE", "EDIT": "FALSE",
        "SEARCH": "FALSE", "ADD": "FALSE", "ESSENTIAL": "FALSE"
    }, {
        "ID": "batch_no", "NAME": u"批编号", "TYPE": "TEXT", "LENGTH": "16",
        "DISPLAY": "TRUE", "EDIT": "TRUE",
        "SEARCH": "TRUE", "ADD": "TRUE", "ESSENTIAL": "FALSE"
    }, {
        "ID": "batch_name", "NAME": u"批名称", "TYPE": "TEXT", "LENGTH": "16",
        "DISPLAY": "TRUE", "EDIT": "TRUE",
        "SEARCH": "TRUE", "ADD": "TRUE", "ESSENTIAL": "FALSE"
    }, {
        "ID": "batch_desc", "NAME": u"批描述", "TYPE": "TEXT", "LENGTH": "16",
        "DISPLAY": "TRUE", "EDIT": "TRUE",
        "SEARCH": "TRUE", "ADD": "TRUE", "ESSENTIAL": "FALSE"
    }, {
        "ID": "comment", "NAME": u"备注", "TYPE": "TEXT", "LENGTH": "16",
        "DISPLAY": "TRUE", "EDIT": "TRUE",
        "SEARCH": "FALSE", "ADD": "TRUE", "ESSENTIAL": "FALSE"
    }, {
        "ID": "create_time", "NAME": u"创建时间", "TYPE": "DATETIME", "LENGTH": "16",
        "DISPLAY": "TRUE", "EDIT": "FALSE",
        "SEARCH": "FALSE", "ADD": "FALSE", "ESSENTIAL": "FALSE"
    }, {
        "ID": "modify_time", "NAME": u"修改时间", "TYPE": "DATETIME", "LENGTH": "16",
        "DISPLAY": "TRUE", "EDIT": "FALSE",
        "SEARCH": "FALSE", "ADD": "FALSE", "ESSENTIAL": "FALSE"
    }]
tp = StartView()
tp.show()

OrcData.exec_()
