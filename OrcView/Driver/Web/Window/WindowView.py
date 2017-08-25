# coding=utf-8
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Lib.LibShell import OrcDisplayView

from .WindowModel import WindowModel
from .WindowModel import WindowControl


class WindowView(OrcDisplayView):

    def __init__(self):

        OrcDisplayView.__init__(self)

        self.title = u"窗口"

        # 窗口标识
        self._window_id = None

        # 控件定义
        self._def = WidgetDefinition('Window')
        self.main.definition.widget_def = self._def

        # 查询条
        self.main.definition.search_enable = True
        self.main.definition.search_column = 3

        # 主控件
        self.model = WindowModel(self._def)
        self.control = WindowControl(self._def)
        self.view = ViewTable(self.model, self.control)
        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_refresh", name=u'刷新'),
            dict(id="act_search", name=u"查询"),
            dict(id="act_update", name=u"修改", type="CHECK"),
            dict(id="act_delete", name=u"删除")]

        # 初始化界面
        self.main.init_view()

        self.main.setContentsMargins(0, 0, 0, 0)

    def act_refresh(self):
        """
        刷新
        :return:
        """
        self.model.mod_add(None)

    def act_search(self):
        """
        查询
        :return:
        """
        _cond = self.__wid_search_cond.get_cond()
        self.model.mod_search(_cond)

    def act_update(self):
        """
        更新
        :return:
        """
        self.model.basic_editable()

    def act_delete(self):
        """
        删除
        :return:
        """
        if OrcMessage.question(self, u"确认删除"):
                self.display.model.mod_delete()

    def set_window_id(self, p_window_id):
        """
        设置窗口ID
        :param p_window_id:
        :return:
        """
        self._window_id = p_window_id
        self.display.model.mod_search({"window_id": self._window_id})

    def clean(self):
        """
        清空
        :return:
        """
        self._window_id = None
        self.display.model.mod_clean()
