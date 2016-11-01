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

tp = StartView()
qss_file = open('Orcview/Style/default.qss').read()
tp.setStyleSheet(qss_file)
tp.show()

OrcData.exec_()
