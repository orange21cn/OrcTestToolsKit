# coding=utf-8
from OrcLib.LibProgram import OrcFactory
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibCmd import OrcRecordCmd
from OrcLib.LibCmd import WebCmd
from OrcLib.LibCmd import DataCmd

from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibTable import ViewTable
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibShell import OrcDialogView
from OrcView.Lib.LibViewDef import WidgetDefinition

from OrcLibFrame.LibCaseData import CaseData


class DataFlabControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'DataFlag')


class DataFlagModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self, 'DataFlag')

        self._case_data = CaseData()

        self._resource_item = OrcResource('Item')

        # 不可以check
        self.basic_checkable(False)

    def service_add(self, p_data):
        """
        暂不使用
        :param p_data:
        :return:
        """
        pass

    def service_delete(self, p_list):
        """
        暂不使用
        :param p_list:
        :return:
        """
        pass

    def service_update(self, p_data):
        """
        暂不使用
        :param p_data:
        :return:
        """
        pass

    def service_search(self, p_cond):
        """
        查询入口
        :param p_cond:
        :return:
        """
        condition = OrcFactory.create_default_dict(p_cond)

        scope_type = condition.value('TYPE')
        ids = condition.value('IDS')

        if scope_type is None:
            return self._usr_search_item(ids)
        else:
            return self._usr_search_id(scope_type, ids)

    def _usr_search_item(self, p_item_ids):
        """
        输入 item_id 查询
        :param p_item_ids:
        :return:
        """
        # 查询 item
        result = self._resource_item.get(parameter=dict(id=p_item_ids))

        if not ResourceCheck.result_status(result, u"获取 item 数据 %s" % p_item_ids, self._logger):
            return []

        return self.__get_flag_info(result.data)

    def _usr_search_id(self, p_type, p_id):
        """
        输入类型及id查出item_id后再进行查询
        :param p_type:
        :param p_id:
        :return:
        """
        self._case_data.load(p_type, p_id)
        return self.__get_flag_info(self._case_data.get_items())

    @staticmethod
    def __get_flag_info(p_item_list):
        """
        获取数据信息列表
        :param p_item_list:
        :return:
        """
        rtn = []
        record = OrcRecordCmd()

        for _item_data in p_item_list:

            record.item(_item_data)

            # Web 类型数据
            if record.is_web_item():

                cmd = WebCmd(eval(_item_data['item_operate']))

                if not cmd.data:
                    continue

                if cmd.is_page():
                    obj_desc = cmd.get_object_info('page_desc')
                elif cmd.is_widget():
                    obj_desc = cmd.get_object_info('widget_desc')
                elif cmd.is_window():
                    obj_desc = cmd.get_object_info('window_desc')
                else:
                    obj_desc = ''

                _info = dict(
                    id=cmd.cmd_object,
                    flag=cmd.get_flag(),
                    data_flag_type=cmd.cmd_type,
                    item_mode=_item_data['item_mode'],
                    num=cmd.data,
                    desc=obj_desc,
                )

                if _info not in rtn:
                    rtn.append(_info)

            # Data 类型数据
            elif record.is_data_item():

                cmd = DataCmd(eval(_item_data['item_operate']))

                if not cmd.data:
                    continue

                _info = dict(
                    id=cmd.cmd_object,
                    flag=cmd.cmd_object,
                    data_flag_type=record.run_det_type,
                    item_mode=_item_data['item_mode'],
                    num=cmd.data,
                    desc=record.desc,
                )

                if _info not in rtn:
                    rtn.append(_info)

            else:
                pass

        return rtn


class DataFlagView(ViewTable):

    def __init__(self):

        ViewTable.__init__(self, DataFlagModel, DataFlabControl)

        self.title = u'数据标识'

    def search(self, p_id, p_type=None):
        """
        查找
        :param p_type: 作用域类型
        :param p_id: 用途域 ID
        :return:
        """
        cond = dict(TYPE=p_type, IDS=p_id)
        self.model.mod_search(cond)

    def get_data(self):
        """
        获取数据,默认给当前数据
        :return:
        """
        return self.model.mod_get_current_data()


class DataFlagSelector(OrcDialogView):
    """
    弹出框选择器
    """
    def __init__(self):

        OrcDialogView.__init__(self)

        self.title = u'数据标识选择'

        # 控件定义
        self._def = WidgetDefinition('DataFlag')
        self.main.definition.widget_def = self._def

        # 主控件
        self.main.display = DataFlagView()

        # 按钮
        self.main.definition.buttons_def = [
            dict(id="act_submit", name=u"提交"),
            dict(id="act_cancel", name=u"取消")]

        # 初始化控件
        self.main.init_view()

        # +---- Connection ----+
        self.main.display.doubleClicked.connect(self.act_submit)

    def act_submit(self):
        """
        提交
        :return:
        """
        self._data = self.main.display.get_data()
        self.close()

    @staticmethod
    def static_get_data(p_id, p_type=None):
        """
        获取数据
        :param p_type:
        :param p_id:
        :return:
        """
        view = DataFlagSelector()
        view.main.display.search(p_id, p_type)
        view.exec_()

        return view._data
