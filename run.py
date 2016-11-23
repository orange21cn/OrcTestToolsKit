# -*- coding: utf-8 -*-
from PySide.QtGui import QApplication

# User interface
import sys
from OrcView.StartView import StartView

reload(sys)
sys.setdefaultencoding('utf-8')

OrcData = QApplication(sys.argv)

tp = StartView()

tp.show()

OrcData.exec_()
