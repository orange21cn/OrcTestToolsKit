# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibAdd import BaseAdder
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Lib.LibShell import OrcDisplayView
from OrcView.Lib.LibViewDef import WidgetDefinition

from .PageDetModel import PageDetModel
from .PageDetModel import PageDetControl


class PageDetView(OrcDisplayView):
    """
    页面定义
    """
    sig_selected = OrcSignal()

    def __init__(self):

        OrcDisplayView.__init__(self)

        # Current page id
        self._page_id = None

        # 控件定义
        self._def = WidgetDefinition('PageDet')
        self.main.definition.widget_def = self._def

        # 主控件
        self.model = PageDetModel(self._def)
        self.control = PageDetControl(self._def)
        self.view = ViewTable(self.model, self.control)
        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_add", name=u"增加"),
            dict(id="act_delete", name=u"删除"),
            dict(id="act_update", name=u"修改", type="CHECK")]

        # 初始化界面
        self.main.init_view()

        # 单击发送点击事件
        self.view.clicked.connect(self.selected)

        self.main.setContentsMargins(0, 0, 0, 0)

    def act_add(self):
        """
        新增
        :return:
        """
        if self._page_id is None:
            return
        page_det_data = PageDetAdder.static_get_data()
        if page_det_data is not None:
            page_det_data["page_id"] = self._page_id
            self.model.mod_add(page_det_data)

    def act_delete(self):
        """
        删除
        :return:
        """
        if OrcMessage.question(self, u"确认删除"):
            self.model.mod_delete()

    def act_update(self):
        """
        修改
        :return:
        """
        self.model.basic_editable()

    def set_page_id(self, p_page_id):
        """
        设置页面 id
        :param p_page_id:
        :return:
        """
        self._page_id = p_page_id
        self.model.mod_search(dict(page_id=self._page_id))

    def selected(self):
        """
        选择后发信号
        :return:
        """
        self.sig_selected.emit()

    def clean(self):
        """
        清理
        :return:
        """
        self.model.mod_clean()


class PageDetAdder(BaseAdder):
    """
    新增计划控件
    """
    def __init__(self):

        BaseAdder.__init__(self, 'PageDet')

        self.setWindowTitle(u'新增页面')

    @staticmethod
    def static_get_data():

        view = PageDetAdder()
        view.exec_()

        return view._data
