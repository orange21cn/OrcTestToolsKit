# coding=utf-8
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcView.Case.Step.ItemView import ItemView
from OrcView.Case.Step.StepView import StepView


class StepContainer(QWidget):

    def __init__(self, p_data):

        QWidget.__init__(self)

        _step_no = p_data["no"]
        _step_id = p_data["id"]
        self.title = _step_no

        self._wid_step = StepView(_step_id)
        self._wid_item = ItemView()

        _layout = QVBoxLayout()
        _layout.addWidget(self._wid_step)
        _layout.addWidget(self._wid_item)

        _layout.setSpacing(0)

        self.setLayout(_layout)

        self._wid_step.sig_select.connect(self._wid_item.set_step_id)
        self._wid_step.sig_delete.connect(self._wid_item.clean)
