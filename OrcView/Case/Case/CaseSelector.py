# coding=utf-8
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibViewDef import ViewDefinition
from OrcView.Lib.LibShell import OrcBasicSelector

from .CaseModel import CaseModel
from .CaseModel import CaseControl


class CaseSelector(OrcBasicSelector):
    """
    计划选取
    """
    def __init__(self):

        OrcBasicSelector.__init__(self)

        self.title = u"用例选择"

        # 界面定义
        self._def = ViewDefinition('Case')

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
        self.model = CaseModel(self._def)
        self.control = CaseControl(self._def)
        self.display = ViewTree(self.model, self.control)

        # 取消可选择选项
        self.model.basic_checkable(False)

        self.init_view()

        # 多选模式,默认关闭
        self._multi = False

    def _operate(self, p_flag):
        """
        点击按钮后操作
        :return:
        """
        if 'search' == p_flag:
            self.model.mod_search(self.searcher.get_cond())
        if 'submit' == p_flag:
            if self._multi:
                self._data = self.model.mod_get_checked()
            else:
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