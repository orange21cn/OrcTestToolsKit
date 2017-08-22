# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from OrcLib.LibProgram import orc_singleton
from OrcView.Data.Data.DataAdd import DataAdder
from OrcView.Lib.LibAdd import ViewNewAdd
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibMessage import OrcMessage
from OrcView.Lib.LibShell import OrcBasicView
from OrcView.Lib.LibViewDef import ViewDefinition

from .BatchDefModel import BatchDefModel
from .BatchDefModel import BatchDefControl


@orc_singleton
class BatchDefView(OrcBasicView):

    sig_batch_det = OrcSignal(dict)

    def __init__(self):

        OrcBasicView.__init__(self)

        self.title = u"计划管理"

        # 显示定义
        self._def = ViewDefinition('BatchDef')

        # 加入查询条
        self._searcher_enable = True

        # 主显示区
        self.model = BatchDefModel(self._def)
        self.control = BatchDefControl(self._def)
        self.display = ViewTree(self.model, self.control)

        # 按钮定义
        self._buttons_def = [
            dict(id="add", name=u"增加"),
            dict(id="delete", name=u"删除"),
            dict(id="update", name=u"修改", type="CHECK"),
            dict(id="search", name=u"查询")
        ]

        # 右键菜单
        self._context_def = [
            dict(NAME=u"增加", STR="sig_add"),
            dict(NAME=u"删除", STR="sig_del"),
            dict(NAME=u"增加数据", STR="sig_data"),
            dict(NAME=u"添加至运行", STR="sig_run")]

        # 初始化界面
        self.init_view()

        # +---- connection ----+
        # 打开明细界面
        self.display.doubleClicked.connect(self._detail)

    def _operate(self, p_flag):
        """
        点击按钮操作
        :param p_flag:
        :return:
        """
        if "add" == p_flag:
            _data = BatchDefAdder.static_get_data()
            if _data is not None:
                self.model.mod_add(_data)
        elif "delete" == p_flag:
            if OrcMessage.question(self, u'确认删除'):
                self.model.mod_delete()
        elif "update" == p_flag:
            self.model.basic_editable()
        elif "search" == p_flag:
            self.model.mod_search(self.searcher.get_cond())
            self.display.resizeColumnToContents(0)
        else:
            pass

    def _context(self, p_flag):
        """
        右键菜单
        :param p_flag:
        :return:
        """
        if "sig_data" == p_flag:
            _id = self.display.model.mod_get_current_data()["id"]
            DataAdder.static_add_data('BATCH', _id)

        elif "sig_run" == p_flag:

            batch_id = self.display.model.mod_get_current_data()["id"]
            self.model.service_run(batch_id)

    def _detail(self, p_index):
        """
        双击操作
        :return:
        """
        if not self.model.mod_get_editable():
            _data = self.model.node(p_index).content
            self.sig_batch_det[dict].emit(dict(id=_data['id'], no=_data['batch_no']))


class BatchDefAdder(ViewNewAdd):
    """
    新增计划控件
    """
    def __init__(self):

        ViewNewAdd.__init__(self, 'BatchDef')

    @staticmethod
    def static_get_data():

        view = BatchDefAdder()
        view.exec_()

        return view._data
