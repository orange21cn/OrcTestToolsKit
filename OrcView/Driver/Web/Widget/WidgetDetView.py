# coding=utf-8
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibAdd import BaseAdder
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Lib.LibShell import OrcDisplayView

from .WidgetDetModel import WidgetDetModel
from .WidgetDetModel import WidgetDetControl


class WidgetDetView(OrcDisplayView):

    def __init__(self):

        OrcDisplayView.__init__(self)

        # Current widget id
        self._widget_info = None

        # 控件定义
        self._def = 'WidgetDet'
        self.main.definition.widget_def = self._def

        # 主控件
        self.model = WidgetDetModel(self._def)
        self.control = WidgetDetControl(self._def)
        self.view = ViewTable(self.model, self.control)
        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_add", name=u"增加"),
            dict(id="act_delete", name=u"删除"),
            dict(id="act_update", name=u"修改", type="CHECK"),
            dict(id="act_up", name=u"上移"),
            dict(id="act_down", name=u"下移")]

        # 初始化界面
        self.main.setContentsMargins(0, 0, 0, 0)
        self.main.init_view()

    def act_add(self):
        """
        新增
        :return:
        """
        if self._widget_info is None:
            return
        _data = WidgetDetAdder.static_get_data()
        if _data is not None:
            _data["widget_id"] = self._widget_info['id']
            self.model.mod_add(_data)

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

    def act_up(self):
        """
        上移
        :return:
        """
        self.model.mod_up()

    def act_down(self):
        """
        下移
        :return:
        """
        self.model.mod_down()

    def set_widget(self, p_widget_info):
        """
        设置控件 id
        :param p_widget_info:
        :return:
        """
        self._widget_info = p_widget_info
        self.model.mod_search({"widget_id": self._widget_info['id']})


class WidgetDetAdder(BaseAdder):
    """
    新增计划控件
    """
    def __init__(self):

        BaseAdder.__init__(self, 'WidgetDet')

        self.setWindowTitle(u'新增控件属性')

    @staticmethod
    def static_get_data():

        view = WidgetDetAdder()
        view.exec_()

        return view._data
