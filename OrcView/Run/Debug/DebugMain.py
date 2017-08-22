# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QSplitter
from PySide.QtCore import Qt

from OrcLib.LibLog import OrcLog
from OrcView.Lib.LibSearch import OrcButtons
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibControl import ControlBase

from OrcView.Data.Data.DataModel import DataControl
from OrcView.Data.Data.DataModel import DataModel
from OrcView.Run.Run.RunDetModel import RunDetControl
from OrcView.Run.Run.RunDetModel import RunDetModel
from OrcView.Data.Data.DataAdd import DataAdder
from OrcView.Driver.Cmd.DataFlagSelector import DataFlagView

from OrcLib.LibCmd import OrcRecordCmd
from OrcLib.LibNet import OrcResource

from .DebugService import DebugService


class DebugObjectModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self, 'WidgetDef')

        self.__logger = OrcLog('view.run.debug.debug_model')

        self.__resource = OrcResource('WidgetDef')

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        pass

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        pass

    def service_update(self, p_data):
        """
        修改
        :param p_data:
        :return:
        """
        pass

    def service_search(self, p_cond=None):
        """
        查询
        :param p_cond:
        :return:
        """
        result = self.__resource.get(parameter=p_cond)

        return result.data


class DebugObjectControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'WidgetDef')


class DebugMain(QWidget):

    def __init__(self):

        QWidget.__init__(self)

        self.title = u'调试'

        # 执行显示
        self.run_det = ViewTree(RunDetModel, RunDetControl)

        # 数据标识控件显示
        # self.object_disp = ViewTable('', DebugObjectModel, DebugObjectControl)
        self.object_disp = DataFlagView()

        # 数据显示
        self.data_disp = ViewTable(DataModel, DataControl)

        # 数据增加
        self.data_add = DataAdder()

        # Buttons window
        self.buttons = OrcButtons([
            dict(id="add", name=u'增加数据'),
            dict(id="delete", name=u"删除数据"),
            dict(id="update", name=u"修改数据")
        ])

        # 布局
        layout_top = QSplitter()
        layout_top.addWidget(self.run_det)
        layout_top.addWidget(self.object_disp)

        layout_disp = QSplitter()
        layout_disp.setOrientation(Qt.Vertical)
        layout_disp.addWidget(layout_top)
        layout_disp.addWidget(self.data_disp)

        layout_main = QVBoxLayout()
        layout_main.addWidget(layout_disp)
        layout_main.addWidget(self.buttons)

        layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_main)

        # +---- connection ----+
        # 单击测试记录后更新界面数据
        self.run_det.sig_selected.connect(self.usr_update_data)

        # 点击数据对象后更新数据标识
        self.object_disp.sig_selected.connect(self.set_object)

        # 点击按钮后操作
        self.buttons.sig_clicked.connect(self._operate)

        # self.data_add.sig_submit.connect()

        # service
        self.service = DebugService()

    def _operate(self, p_flag):
        """
        点击按钮后制作
        :param p_flag:
        :return:
        """
        if 'add' == p_flag:
            self.data_add.show()
            self.data_disp.model.mod_refresh

        elif 'delete' == p_flag:
            self.data_disp.model.mod_delete()

        elif 'update' == p_flag:
            self.data_disp.model.set_enable()

        else:
            pass

    def usr_refresh(self, p_path=None):
        """
        刷新run_det列表并把根节点在总列表中的路径传给 service,用于数据显示
        :param p_path:
        :return:
        """
        # 调置根节点
        root_node = self.run_det.model.mod_get_root()

        if root_node is not None:
            self.service.set_root(root_node.content)
        else:
            return

        # 更新用例列表
        self.run_det.model.mod_search(dict(path=p_path))

    def usr_update_data(self, p_data):
        """
        更新界面数据
        :param p_data:
        :return:
        """
        run_cmd = OrcRecordCmd(p_data)

        # 获取对象列表
        item_ids = [item['id'] for item in self.run_det.model.service_get_item_list(run_cmd.id)]
        item_ids = list(set(item_ids))

        # 更新对象界面
        self.object_disp.model.mod_search(dict(IDS=item_ids))

        # 获取数据源列表
        path_list = self.service.get_src_ids(
            self.run_det.model.service_get_path(run_cmd.id))

        # 更新数据源数据
        self.data_disp.model.mod_search(dict(src_id=path_list))

        # 设置新增数据数据源类型
        if run_cmd.is_batch_type():
            self.data_add.set_src_type('BATCH')
        elif run_cmd.is_case_type():
            self.data_add.set_src_type('CASE')
        elif run_cmd.is_step_type():
            self.data_add.set_src_type('STEP')
        else:
            self.data_add.set_src_type('ITEM')

        # 设置新增数据数据源 id
        self.data_add.set_src_id(run_cmd.id)

        # 清空新增数据数据标识
        self.data_add.clean_data('data_flag')

    def set_object(self, p_data):
        """
        设置对象
        :param p_data:
        :return:
        """
        self.data_add.set_flag(p_data)
        self.data_add.set_enable('data_flag', False)
