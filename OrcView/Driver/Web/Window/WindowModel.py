# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTable import ModelTable


class WindowModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self, 'Window')

        self.__logger = LogClient()

        self.__resource_widget_def = OrcResource("WidgetDef")
        self.__resource_widow_def = OrcResource("WindowDef")

    def service_add(self, p_data):
        """
        把存在于 widget 表但在 window 表中不存在的 window 增加到 window 表
        :param p_data:
        :return:
        """
        # 查找控件定论中的 window
        result_win_widget = self.__resource_widget_def.get(parameter=dict(widget_type="WINDOW"))

        # 检查结果
        if not ResourceCheck.result_status(result_win_widget, u"查询窗口控件", self.__logger):
            return dict()

        if not result_win_widget.data:
            return

        # 查询 window 模块中已有的 window
        result_win_window = self.__resource_widow_def.get()

        # 检查结果
        if not ResourceCheck.result_status(result_win_window, u"查询现有窗口", self.__logger):
            return dict()

        win_id_all = [item["id"] for item in result_win_widget.data]
        win_id_exist = [item["id"] for item in result_win_window.data]

        for _id in win_id_all:
            if (not win_id_exist) or (_id not in win_id_exist):

                result = self.__resource_widow_def.post(parameter=dict(id=_id))

                # 检查结果
                if not ResourceCheck.result_status(result, u"新增窗口", self.__logger):
                    return list()

        # 打印成功信息
        ResourceCheck.result_success(u"新增窗口", self.__logger)

        return dict()

    def service_delete(self, p_list):
        """
        :param p_list:
        :return:
        """
        result = self.__resource_widow_def.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除窗口", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除窗口", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        :param p_data:
        :return:
        """
        result = self.__resource_widow_def.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新窗口", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新窗口", self.__logger)

        return result.status

    def service_search(self, p_cond):
        """
        :param p_cond:
        :return:
        """
        cond = p_cond

        # 有 window_flag 条件先查 widget
        if "window_flag" in cond:

            result_widget = self.__resource_widget_def.get(
                parameter=dict(widget_flag=cond["window_flag"]))

            # 检查结果
            if not ResourceCheck.result_status(result_widget, u"查询窗口标识", self.__logger):
                return False

            _ids = [item["id"] for item in result_widget.data]
            cond["id"] = _ids

        # 查询
        result_window = self.__resource_widow_def.get(cond)

        # 检查结果
        if not ResourceCheck.result_status(result_window, u"查询窗口标识", self.__logger):
            return list()

        result_window_list = self.__resource_widget_def.get(dict(widget_type="WINDOW"))

        # 检查结果
        if not ResourceCheck.result_status(result_window_list, u"查询窗口标识", self.__logger):
            return list()

        def _get_widget(p_id):
            for _item in result_window_list.data:
                if _item["id"] == p_id:
                    return _item
            return None

        if result_window.data is None:
            return []

        for _window in result_window.data:

            _widget = _get_widget(_window["id"])

            if _widget is not None:

                _window["window_flag"] = _widget["widget_flag"]

        return result_window.data