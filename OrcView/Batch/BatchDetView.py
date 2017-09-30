# coding=utf-8
from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibMessage import OrcMessage

from .BatchDetModel import BatchDetModel
from .BatchDetModel import BatchDetControl
from OrcView.Case.Case.CaseSelector import CaseSelector


class BatchDetView(OrcDisplayView):

    def __init__(self, p_data):

        OrcDisplayView.__init__(self)

        self._batch_id = p_data["id"]
        self.title = p_data["no"]

        # 控件定义
        self._def = WidgetDefinition('BatchDet')
        self.main.definition.widget_def = self._def

        # 查询条件
        self.main.definition.search_enable = True

        # 主控件
        self.model = BatchDetModel(self._def)
        self.control = BatchDetControl(self._def)
        self.view = ViewTable(self.model, self.control)

        self.main.display = self.view

        # 分页
        self.main.definition.pagination_enable = True

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_add", name=u"增加"),
            dict(id="act_delete", name=u"删除"),
            dict(id="act_search", name=u"查询")]

        # 初始化界面
        self.main.init_view()

    def act_add(self):
        """
        新增
        :return:
        """
        _data = CaseSelector.static_get_multi_data()
        if _data is None:
            return

        ids = [_item['id'] for _item in _data]
        self.model.mod_add(dict(batch_id=self._batch_id, case=ids))

    def act_delete(self):
        """
        删除
        :return:
        """
        if OrcMessage.question(self, u"确认删除"):
            self.model.mod_delete()

    def act_search(self):
        """
        查询
        :return:
        """
        self.main.basic_search(self.model.mod_search, dict(batch_id=self._batch_id))
