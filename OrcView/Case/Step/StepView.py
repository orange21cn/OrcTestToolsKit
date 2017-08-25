# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from OrcLib.LibType import DirType
from OrcView.Data.Data.DataAdd import DataAdder
from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Lib.LibAdd import BaseAdder
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibMessage import OrcMessage

from .StepModel import StepModel
from .StepModel import StepControl


class StepView(OrcDisplayView):
    """
    步骤显示界面
    """
    # 单击信号,用于外部更新步骤项
    sig_select = OrcSignal(int)

    # 删除信号,用于外部更新界面
    sig_delete = OrcSignal()

    def __init__(self, p_id):

        OrcDisplayView.__init__(self)

        self._case_id = p_id

        # 布局方向
        self.main.definition.direction = DirType.HORIZON

        # 控件定义
        self._def = WidgetDefinition('Step')
        self.main.definition.widget_def = self._def

        # 主显示区
        self.model = StepModel()
        self.control = StepControl()
        self.view = ViewTable(self.model, self.control)
        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_dir = DirType.VERTICAL
        self.main.definition.buttons_def = [
            dict(id="act_add", name=u"增加"),
            dict(id="act_delete", name=u"删除"),
            dict(id="act_update", name=u"修改", type="CHECK"),
            dict(id="act_up", name=u"上移"),
            dict(id="act_down", name=u"下移")]

        # 右键菜单
        self.main.definition.context_def = [
            dict(NAME=u"增加", STR="act_add"),
            dict(NAME=u"复制", STR="act_duplicate"),
            dict(NAME=u"删除", STR="act_delete"),
            dict(NAME=u"增加数据", STR="act_data")]

        # 初始化界面
        self.main.init_view()
        self.main.setContentsMargins(0, 0, 0, 0)

        # 初始化界面数据
        self.model.mod_search(dict(case_id=p_id))

        # +---- Connection ----+
        # 单击发出单击事件
        self.view.clicked.connect(self.act_selected)

    def act_add(self):
        """
        新增
        :return:
        """
        _data = StepAdder.static_get_data()
        if _data is not None:
            self.model.mod_add(dict(case_det=dict(case_id=self._case_id), step=_data))

    def act_duplicate(self):
        """
        复制
        :return:
        """
        _data = self.model.mod_get_current_data()
        if not _data:
            return
        _data.pop('id')
        self.model.mod_add(_data)

    def act_delete(self):
        """
        删除
        :return:
        """
        if OrcMessage.question(self, u'确认删除'):
            self.model.mod_delete()
            self.sig_delete.emit()

    def act_update(self):
        """
        更新
        :return:
        """
        self.model.basic_editable()

    def act_up(self):
        """
        上移
        :return:
        """
        self.model.mod_up()

    def act_down(self):
        """
        下移
        :return:
        """
        self.model.mod_down()

    def act_data(self):
        """
        增加数据
        :return:
        """
        _data = self.model.mod_get_current_data()
        if _data is not None:
            DataAdder.static_add_data("STEP", _data['step_id'])

    def act_selected(self):
        """
        发出单击事件用于显示步骤执行项
        :return:
        """
        _data = self.model.mod_get_current_data()
        if _data:
            self.sig_select.emit(_data['step_id'])


class StepAdder(BaseAdder):
    """
    新增计划控件
    """
    def __init__(self):

        BaseAdder.__init__(self, 'Step')

        self.setWindowTitle(u'新增步骤')

    @staticmethod
    def static_get_data():

        view = StepAdder()
        view.exec_()

        return view._data
