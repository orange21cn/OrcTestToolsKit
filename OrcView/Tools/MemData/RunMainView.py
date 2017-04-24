from PySide.QtGui import QWidget
from PySide.QtGui import QTabWidget

from .RunTimeView import RunTimeDispView
from .RunDataView import RunDataDispView


class RunMainView(QTabWidget):
    """

    """
    def __init__(self):

        QTabWidget.__init__(self)

        view_time = RunTimeDispView()
        view_data = RunDataDispView()

        self.addTab(view_time, 'abc')
        self.addTab(view_data, 'def')