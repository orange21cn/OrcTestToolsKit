# coding=utf-8
from OrcLib.LibProgram import orc_singleton
from OrcView.Data.Data.DataModel import DataModel
from OrcView.Data.Data.DataAdd import DataAdder
from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibMessage import OrcMessage

from .DataModel import DataControl


@orc_singleton
class DataView(OrcDisplayView):
    """
    View of table
    """
    def __init__(self):

        OrcDisplayView.__init__(self)

        self.title = u"数据管理"

        # 控件定义
        self._def = WidgetDefinition('Data')
        self.main.definition.widget_def = self._def

        # 查询框
        self.main.definition.search_enable = True
        self.main.definition.search_column = 3

        # 主控件
        self.model = DataModel(self._def)
        self.control = DataControl(self._def)
        self.view = ViewTable(self.model, self.control)
        self.main.display = self.view

        # 分页
        self.main.definition.pagination_enable = True

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_add", name=u"增加"),
            dict(id="act_delete", name=u"删除"),
            dict(id="act_update", name=u"修改", type="CHECK"),
            dict(id="act_search", name=u"查询")]

        # 初始化界面
        self.main.init_view()

    def act_add(self):
        """
        新增
        :return:
        """
        DataAdder.static_add_data()
        self.model.mod_refresh()

    def act_delete(self):
        """
        删除
        :return:
        """
        if OrcMessage.question(self, u'确认删除'):
            self.model.mod_delete()

    def act_update(self):
        """
        修改
        :return:
        """
        self.model.basic_editable()

    def act_search(self):
        """
        查询
        :return:
        """
        self.main.basic_search(self.model.mod_search)
