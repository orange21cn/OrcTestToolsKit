# coding=utf-8
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QWidget

from OrcView.Case.Step.ItemView import ItemView
from OrcView.Case.Step.StepView import StepView


class StepContainer(QWidget):

    def __init__(self, p_data):

        QWidget.__init__(self)

        # 步骤编号
        step_no = p_data["no"]

        # 步骤 ID
        step_id = p_data["id"]

        # 界面 title
        self.title = step_no

        # 步骤显示界面
        self._wid_step = StepView(step_id)

        # 步骤项显示界面
        self._wid_item = ItemView()

        # 布局
        layout_main = QVBoxLayout()
        layout_main.addWidget(self._wid_step)
        layout_main.addWidget(self._wid_item)

        layout_main.setSpacing(0)

        self.setLayout(layout_main)

        # 步骤界面显示后更新步骤项界面
        self._wid_step.sig_select.connect(self._wid_item.set_step_id)

        # 步骤删除后清除步骤项界面
        self._wid_step.sig_delete.connect(self._wid_item.clean)
