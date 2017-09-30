# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Lib.LibAdd import BaseAdder
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Data.Data.DataAdd import DataAdder

from .CaseModel import CaseModel
from .CaseModel import CaseControl


class CaseView(OrcDisplayView):

    sig_case_det = OrcSignal(dict)

    def __init__(self):

        OrcDisplayView.__init__(self)

        self.title = u"用例管理"

        # 控件定义
        self._def = WidgetDefinition('Case')
        self.main.definition.widget_def = self._def

        # 查询
        self.main.definition.search_enable = True

        # 主控件
        self.model = CaseModel(self._def)
        self.control = CaseControl(self._def)
        self.view = ViewTree(self.model, self.control)

        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_def = [
                dict(id='act_add', name=u'增加'),
                dict(id='act_delete', name=u'删除'),
                dict(id='act_update', name=u'修改', type='CHECK'),
                dict(id='act_search', name=u'查询')]

        # 右键菜单
        self.main.definition.context_def = [
                dict(NAME=u'增加', STR='act_add'),
                dict(NAME=u'复制', STR='act_duplicate'),
                dict(NAME=u'删除', STR='act_delete'),
                dict(NAME=u'增加数据', STR='act_data'),
                dict(NAME=u'添加至运行', STR='act_run')]

        # 初始化界面
        self.main.init_view()

        # +---- Connection ----+
        # 双击打开用例发双击信号
        self.view.doubleClicked.connect(self.act_detail)

    def act_add(self):
        """
        新增
        :return:
        """
        _data = CaseDefAdder.static_get_data()
        if _data is not None:
            self.model.mod_add(_data)

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

    def act_update(self):
        """
        更新
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
        _data = self.model.mod_get_current_data()
        if _data:
            DataAdder.static_add_data('CASE', _data['id'])

    def act_run(self):
        """
        添加至执行
        :return:
        """
        _data = self.model.mod_get_current_data()
        if _data:
            self.model.service_run(_data['id'])

    def act_detail(self, p_index):
        """
        双击信号用于展开用例步骤界面
        :param p_index:
        :return:
        """
        if self.model.mod_get_editable():
            return

        _data = self.model.node(p_index).content

        if not _data:
            return

        if _data['case_type'] in ('CASE_SUITE', 'FUNC_SUITE'):
            return

        self.sig_case_det[dict].emit(dict(id=_data['id'], no=_data['case_no']))


class CaseDefAdder(BaseAdder):
    """
    新增计划控件
    """
    def __init__(self):

        BaseAdder.__init__(self, 'Case')

        self.setWindowTitle(u'新增用例')

    @staticmethod
    def static_get_data():

        view = CaseDefAdder()
        view.exec_()

        return view._data
