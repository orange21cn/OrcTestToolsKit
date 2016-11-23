# coding=utf-8

from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout

from OrcView.Case.CaseDet import ViewCaseDetMag
from OrcView.Case.StepDet import ViewStepDetMag


class StepContainer(QWidget):

    def __init__(self, p_data):

        QWidget.__init__(self)

        _step_no = p_data["no"]
        _step_id = p_data["id"]
        self.title = _step_no

        self._wid_step = ViewCaseDetMag(_step_id)
        self._wid_item = ViewStepDetMag()

        _layout = QVBoxLayout()
        _layout.addWidget(self._wid_step)
        _layout.addWidget(self._wid_item)

        _layout.setSpacing(1)

        self.setLayout(_layout)

        self._wid_step.sig_select.connect(self._wid_item.set_step_id)
        self._wid_step.sig_delete.connect(self._wid_item.clean)
