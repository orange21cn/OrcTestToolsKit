# -*- coding: utf-8 -*-
from PySide.QtGui import QApplication
import sys
from OrcView.Debug.ObjectChecker import ObjectChecker
from OrcView.Lib.LibSearch import ViewButtons
from PySide.QtGui import QGroupBox
from PySide.QtGui import QWidget
from PySide.QtGui import QPushButton
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QScrollArea


OrcData = QApplication(sys.argv)

tp = ObjectChecker()

tp.show()

OrcData.exec_()
