# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.dirname(__file__))

from PySide.QtGui import QApplication
from OrcView.StartView import StartView


OrcData = QApplication(sys.argv)

tp = StartView()
tp.show()

OrcData.exec_()
