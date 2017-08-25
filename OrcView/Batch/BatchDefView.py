# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from OrcLib.LibProgram import orc_singleton
from OrcView.Data.Data.DataAdd import DataAdder
from OrcView.Lib.LibAdd import BaseAdder
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibViewDef import WidgetDefinition

from .BatchDefModel import BatchDefModel
from .BatchDefModel import BatchDefControl


@orc_singleton
class BatchDefView(OrcDisplayView):

    sig_batch_det = OrcSignal(dict)

    def __init__(self):

        OrcDisplayView.__init__(self)

        self.title = u"计划管理"

        # 显示定义
        self._def = WidgetDefinition('BatchDef')
        self.main.definition.widget_def = self._def

        # 加入查询条
        self.main.definition.search_enable = True

        # 主显示区
        self.model = BatchDefModel(self._def)
        self.control = BatchDefControl(self._def)
        self.view = ViewTree(self.model, self.control)
        self.main.display = self.view

        # 按钮定义
        self.main.definition.buttons_def = [
            dict(id="act_add", name=u"增加"),
            dict(id="act_delete", name=u"删除"),
            dict(id="act_update", name=u"修改", type="CHECK"),
            dict(id="act_search", name=u"查询")]

        # 右键菜单
        self.main.definition.context_def = [
            dict(NAME=u"增加", STR="act_add"),
            dict(NAME=u"删除", STR="act_delete"),
            dict(NAME=u"复制", STR="act_duplicate"),
            dict(NAME=u"增加数据", STR="act_data"),
            dict(NAME=u"添加至运行", STR="act_run")]

        # 初始化界面
        self.main.init_view()

        # +---- connection ----+
        # 打开明细界面
        self.view.doubleClicked.connect(self.act_detail)

    def act_add(self):
        """
        新增
        :return:
        """
        _data = BatchDefAdder.static_get_data()
        if _data is not None:
            self.model.mod_add(_data)

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

    def act_data(self):
        """
        增加数据
        :return:
        """
        _id = self.model.mod_get_current_data()["id"]
        DataAdder.static_add_data('BATCH', _id)

    def act_duplicate(self):
        """
        复制
        :return:
        """
        _data = self.model.mod_get_current_data()

        if _data is not None:
            _data.pop('id')
            self.model.mod_add(_data)

    def act_run(self):
        """
        运行
        :return:
        """
        batch_id = self.display.model.mod_get_current_data()["id"]
        self.model.service_run(batch_id)

    def act_detail(self, p_index):
        """
        双击操作
        :param p_index:
        :return:
        """
        if self.model.mod_get_editable():
            return

        _data = self.model.node(p_index).content

        if 'BATCH_SUITE' == _data['batch_type']:
            return

        self.sig_batch_det[dict].emit(dict(id=_data['id'], no=_data['batch_no']))


class BatchDefAdder(BaseAdder):
    """
    新增计划控件
    """
    def __init__(self):

        BaseAdder.__init__(self, 'BatchDef')

    @staticmethod
    def static_get_data():

        view = BatchDefAdder()
        view.exec_()

        return view._data
