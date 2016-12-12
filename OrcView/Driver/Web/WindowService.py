# coding=utf-8
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcHttpNewResource


class WindowDefService:
    """
    Window service
    """
    def __init__(self):

        # Log
        self.__logger = OrcLog("view.driver.web.service.window_def")

        self.__resource_widget_def = OrcHttpNewResource("WidgetDef")
        self.__resource_widow_def = OrcHttpNewResource("WindowDef")

    def usr_add(self, p_data):
        """
        把存在于 widget 表但在 window 表中不存在的 window 增加到 window 表
        :param p_data:
        :return:
        """
        windows_all = [item["id"] for item in self.__resource_widget_def.get(dict(widget_type="WINDOW"))]
        windows_exist = [item["id"] for item in self.__resource_widow_def.get()]

        if not windows_all:
            return

        for _id in windows_all:
            if (not windows_exist) or (_id not in windows_exist):
                self.__resource_widow_def.post(dict(id=_id))

        return dict()

    def usr_delete(self, p_list):
        """
        :param p_list:
        :return:
        """
        return self.__resource_widow_def.delete(p_list)

    def usr_update(self, p_data):
        """
        :param p_data:
        :return:
        """
        self.__resource_widow_def.set_path(p_data["id"])
        return self.__resource_widow_def.put(p_data)

    def usr_search(self, p_cond):
        """
        :param p_cond:
        :return:
        """
        _cond = p_cond

        # 有 window_flag 条件先查 widget
        if "window_flag" in _cond:
            _ids = [item["id"] for item in self.__resource_widget_def.get(dict(widget_flag=_cond["window_flag"]))]
            _cond["id"] = _ids

        # 查询
        _data = self.__resource_widow_def.get(_cond)
        _window_list = self.__resource_widget_def.get(dict(widget_type="WINDOW"))

        def _get_widget(p_id):
            for _item in _window_list:
                if _item["id"] == p_id:
                    return _item
            return None

        if _data is None:
            return []
        else:
            for _window in _data:

                _widget = _get_widget(_window["id"])

                if _widget is not None:

                    _window["window_flag"] = _widget["widget_flag"]

            return _data
