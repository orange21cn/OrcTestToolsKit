# coding=utf-8
from PySide.QtGui import QStackedWidget

from OrcLib.LibType import DriverType
from OrcLib.LibType import DirType
from OrcView.Case.Case.CaseSelector import CaseSelector
from OrcView.Data.Data.DataAdd import DataAdder
from OrcView.Driver.Cmd.CmdCreator import DataCmdCreator
from OrcView.Driver.Cmd.CmdCreator import WebCmdCreator
from OrcView.Lib.LibViewDef import WidgetDefinition
from OrcView.Lib.LibAdd import BaseAdder
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibShell import OrcDisplayView

from .ItemModel import ItemFuncModel
from .ItemModel import ItemNormalModel
from .ItemModel import ItemControl


class ItemView(OrcDisplayView):

    def __init__(self):

        OrcDisplayView.__init__(self)

        self._step_id = None

        # 布局方向
        self.main.definition.direction = DirType.HORIZON

        # 控件定义
        self._def = WidgetDefinition('Item')

        # 主显示控件
        # Item ----
        self.model_item = ItemNormalModel(self._def)
        self.model_func = ItemFuncModel()
        self.control = ItemControl(self._def)

        # Normal
        self.item_display = ViewTable(self.model_item, self.control)

        # Func
        self.func_display = ViewTable(self.model_func, self.control)

        # stack widget
        self.view = QStackedWidget()
        self.view.addWidget(self.item_display)
        self.view.addWidget(self.func_display)

        self.main.display = self.view

        # 按钮
        self.main.definition.buttons_dir = DirType.VERTICAL
        self.main.definition.buttons_def = [
            dict(id='act_add', name=u'增加'),
            dict(id='act_delete', name=u'删除'),
            dict(id='act_update', name=u'修改', type='CHECK'),
            dict(id='act_up', name=u'上移'),
            dict(id='act_down', name=u'下移')]

        # 右键菜单,默认方式不支持复杂界面,这里进行重写
        context_item_def = [
            dict(NAME=u'增加', STR='act_add'),
            dict(NAME=u'复制', STR='act_duplicate'),
            dict(NAME=u'删除', STR='act_delete'),
            dict(NAME=u'增加数据', STR='act_data')]

        context_func_def = [
            dict(NAME=u'增加', STR='act_add'),
            dict(NAME=u'删除', STR='act_delete'),
            dict(NAME=u'增加数据', STR='act_data')]

        self.item_display.create_context_menu(context_item_def)
        self.func_display.create_context_menu(context_func_def)

        self.item_display.sig_context.connect(self._dispatch_context)
        self.func_display.sig_context.connect(self._dispatch_context)

        # default
        self.display = self.item_display
        self.model = self.model_item
        self.step_type = 'STEP_NORMAL'

        self.main.init_view()
        self.main.setContentsMargins(0, 0, 0, 0)

    def _dispatch_context(self, p_flag):
        """
        右键菜单操作
        :param p_flag:
        :return:
        """
        try:
            getattr(self, p_flag)()
        except AttributeError:
            self._logger.error('Right clicked but no func founded')

    def act_add(self):
        """
        新增
        :return:
        """
        if 'STEP_FUNC' == self.step_type:
            _data = CaseSelector.static_get_data()
            if _data is None:
                return
            self.model.mod_add(dict(type='FUNC', step_id=self._step_id, data=_data['id']))

        elif 'STEP_NORMAL' == self.step_type:
            _data = ItemAdder.static_get_data()
            if _data is None:
                return
            self.model.mod_add(dict(type='ITEM', step_id=self._step_id, data=_data))

        else:
            pass

    def act_duplicate(self):
        """
        复制
        :return:
        """
        if 'STEP_NORMAL' == self.step_type:
            item_data = self.model_item.mod_get_current_data()
            if not item_data:
                return
            item_data.pop('id')
            item_data['item_operate'] = eval(item_data['item_operate'])
            _data = dict(type='ITEM', step_id=self._step_id, data=item_data)
            self.model_item.mod_add(_data)

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

    def act_data(self):
        """
        增加数据
        :return:
        """
        _id = self.model.mod_get_current_data()['item_id']
        DataAdder.static_add_data('ITEM', _id)

    def set_step_id(self, p_step_id):
        """
        设置步骤ID
        :param p_step_id:
        :return:
        """
        if p_step_id is None:
            return

        self._step_id = p_step_id
        self.step_type = self.model.service_get_step_type(self._step_id)

        if 'STEP_FUNC' == self.step_type:
            self.display = self.func_display
            self.model = self.model_func
            self.view.setCurrentIndex(1)

        elif 'STEP_NORMAL' == self.step_type:
            self.display = self.item_display
            self.model = self.model_item
            self.view.setCurrentIndex(0)

        else:
            pass

        self.model.mod_search({'step_id': self._step_id})

    def clean(self):
        """
        清理
        :return:
        """
        self._step_id = None
        self.model.mod_clean()


class ItemAdder(BaseAdder):
    """
    新增计划控件
    """
    def __init__(self):

        BaseAdder.__init__(self, 'Item')

        self.setWindowTitle(u'新增步骤项')

    def _action(self, p_flag):
        """
        点击控件后操作
        :param p_flag:
        :return:
        """
        if 'item_operate' == p_flag:

            item_mode = self.get_data('item_mode')
            item_type = self.get_data('item_type')

            if item_type == DriverType.WEB:
                cmd = WebCmdCreator.get_cmd(item_mode)
            elif item_type == DriverType.DATA:
                cmd = DataCmdCreator.get_cmd(item_mode)
            else:
                cmd = None

            self.set_data('item_operate', cmd)

    @staticmethod
    def static_get_data():

        view = ItemAdder()
        view.exec_()

        return view._data
