# coding=utf-8
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibTable import ViewTable

from .DataResDispModel import DataResDispModel


class DataResDispControl(ControlBase):
    """
    sql 结果显示
    """
    def __init__(self):

        ControlBase.__init__(self, '')


class DataResDispView(ViewTable):
    """
    sql 结果显示
    """
    def __init__(self):

        ViewTable.__init__(self, DataResDispModel, DataResDispControl)
