# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(__file__))

from PySide.QtGui import QApplication
from PySide.QtGui import QFileDialog
from OrcView.StartView import StartView
from OrcView.Lib.LibView import OrcFileSelection


OrcData = QApplication(sys.argv)

tp = OrcFileSelection()
tp.show()

OrcData.exec_()
