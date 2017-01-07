# -*- coding: utf-8 -*-
from PySide.QtGui import QApplication

# User interface
import sys
from OrcView.StartView import StartView


OrcData = QApplication(sys.argv)

tp = StartView()
tp.show()

OrcData.exec_()
