# coding=utf-8
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibShell import OrcDialogView
from OrcView.Lib.LibViewDef import WidgetDefinition

from .WidgetDefModel import WidgetDefModel
from .WidgetDefModel import WidgetDefControl


class WidgetSelector(OrcDialogView):
    """
    控件选择器
    """
    def __init__(self):

        OrcDialogView.__init__(self)

        # 控件定义
        self._def = WidgetDefinition('WidgetDef')
        self.main.definition.widget_def = self._def

        # 查询
        self.main.definition.search_enable = True
        self.main.definition.search_column = 2

        # 主控件
        self.model = WidgetDefModel(self._def)
        self.control = WidgetDefControl(self._def)
        self.view = ViewTree(self.model, self.control)
        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_search", name=u"查询"),
            dict(id="act_submit", name=u"选择"),
            dict(id="act_cancel", name=u"取消")]

        # 禁止选择
        self.model.basic_checkable(False)

        # 初始化界面
        self.main.init_view()

        # +---- Connection ----+
        self.view.doubleClicked.connect(self.act_submit)

    def act_search(self):
        """
        查询
        :return:
        """
        self.model.mod_search(self.main.searcher.get_cond())

    def act_submit(self):
        """
        提交
        :return:
        """
        self._data = self.model.mod_get_current_data()
        self.close()

    @staticmethod
    def get_widget():
        """

        :return:
        """
        view = WidgetSelector()
        view.exec_()

        return view._data
