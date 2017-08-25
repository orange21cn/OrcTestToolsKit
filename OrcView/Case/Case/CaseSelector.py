# coding=utf-8
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Lib.LibShell import OrcDialogView

from .CaseModel import CaseModel
from .CaseModel import CaseControl


class CaseSelector(OrcDialogView):
    """
    计划选取
    """
    def __init__(self):

        OrcDialogView.__init__(self)

        self.title = u"用例选择"

        # 界面定义
        self._def = WidgetDefinition('Case')

        self._def.field('create_time').set_displayable(False)
        self._def.field('modify_time').set_displayable(False)
        self._def.field('comment').set_displayable(False)

        self.main.definition.widget_def = self._def

        # 查询条
        self.main.definition.search_enable = True
        self.main.definition.search_column = 2

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_search", name=u"查询"),
            dict(id="act_submit", name=u"选择"),
            dict(id="act_cancel", name=u"取消")]

        # 主显示控件
        self.model = CaseModel(self._def)
        self.control = CaseControl(self._def)
        self.view = ViewTree(self.model, self.control)
        self.main.display = self.view

        # 初始化界面
        self.main.init_view()

        # 取消可选择选项
        self.model.basic_checkable(False)

        # +---- Connection ----+
        self.view.doubleClicked.connect(self.act_submit)

        # 多选模式,默认关闭
        self._multi = False

    def act_search(self):
        """
        查询
        :return:
        """
        self.main.basic_search(self.model.mod_search)

    def act_submit(self):
        """
        提交
        :return:
        """
        if self._multi:
            self._data = self.model.mod_get_checked()
        else:
            self._data = self.model.mod_get_current_data()
        self.close()

    @staticmethod
    def static_get_data():
        """
        静态获取数据
        :return:
        """
        view = CaseSelector()
        view.exec_()

        return view._data

    @staticmethod
    def static_get_multi_data():
        """
        静态获取数据
        :return:
        """
        view = CaseSelector()
        view._multi = True
        view.model.basic_checkable(True)
        view.exec_()

        return view._data
