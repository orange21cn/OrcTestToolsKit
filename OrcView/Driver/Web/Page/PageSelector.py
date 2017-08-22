# coding=utf-8
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibViewDef import ViewDefinition
from OrcView.Lib.LibShell import OrcBasicSelector

from .PageDefModel import PageDefModel
from .PageDefModel import PageDefControl


class PageSelector(OrcBasicSelector):
    """
    计划选取
    """
    def __init__(self):

        OrcBasicSelector.__init__(self)

        self.title = u"页面选择"

        # 界面定义
        self._def = ViewDefinition('PageDef')

        self._def.field('create_time').set_displayable(False)
        self._def.field('modify_time').set_displayable(False)
        self._def.field('comment').set_displayable(False)

        # 查询条
        self._search_enable = True
        self._search_column = 2

        # 按钮
        self._buttons_def = [
            dict(id="search", name=u"查询"),
            dict(id="submit", name=u"提交"),
            dict(id="cancel", name=u"取消")]

        # 主显示控件
        self.model = PageDefModel(self._def)
        self.control = PageDefControl(self._def)
        self.display = ViewTable(self.model, self.control)

        # 取消可选择选项
        self.model.basic_checkable(False)

        self.init_view()

    def _operate(self, p_flag):
        """
        点击按钮后操作
        :return:
        """
        if 'search' == p_flag:
            self.model.mod_search(self.searcher.get_cond())
        if 'submit' == p_flag:
            self._data = self.model.mod_get_current_data()
            self.close()
        elif 'cancel' == p_flag:
            self.close()
        else:
            pass

    @staticmethod
    def static_get_data():
        """
        静态获取数据
        :return:
        """
        view = PageSelector()
        view.exec_()

        return view._data
