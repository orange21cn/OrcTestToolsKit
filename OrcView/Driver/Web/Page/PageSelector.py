# coding=utf-8
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Lib.LibShell import OrcDialogView

from .PageDefModel import PageDefModel
from .PageDefModel import PageDefControl


class PageSelector(OrcDialogView):
    """
    计划选取
    """
    def __init__(self):

        OrcDialogView.__init__(self)

        self.title = u"页面选择"

        # 界面定义
        self._def = WidgetDefinition('PageDef')

        self._def.field('create_time').set_displayable(False)
        self._def.field('modify_time').set_displayable(False)
        self._def.field('comment').set_displayable(False)

        self.main.definition.widget_def = self._def

        # 查询条
        self.main.definition.search_enable = True
        self.main.definition.search_column = 2

        # 主显示控件
        self.model = PageDefModel(self._def)
        self.control = PageDefControl(self._def)
        self.view = ViewTable(self.model, self.control)
        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_search", name=u"查询"),
            dict(id="act_submit", name=u"提交"),
            dict(id="act_cancel", name=u"取消")]

        # 取消可选择选项
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
    def static_get_data():
        """
        静态获取数据
        :return:
        """
        view = PageSelector()
        view.exec_()

        return view._data
