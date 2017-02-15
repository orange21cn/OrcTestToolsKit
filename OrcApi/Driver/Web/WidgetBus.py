# coding=utf-8
from OrcLib.LibApi import OrcBus
from OrcLib.LibException import OrcApiModelFailException

from WidgetDefMod import WidgetDefMod
from WidgetDetMod import WidgetDetMod


class WidgetDefBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "widget_def", WidgetDefMod)

        self.__bus_widget_det = WidgetDetBus()

    def bus_list_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        result = []

        mode = p_cond["type"] if "type" in p_cond else None
        widget_id = p_cond["id"] if "id" in p_cond else None

        try:
            # 查询符合条件的整用例树,至根节点
            if "all" == mode:
                result = self._model.usr_search_all(p_cond)

            # 查询节点及子节点
            elif "tree" == mode:
                if widget_id is not None:
                    result = self._model.usr_search_tree(widget_id)

            # 查询节点路径
            elif "path" == mode:
                if widget_id is not None:
                    result = self._model.usr_search_path(widget_id)

            # 其他情况只查询符合条件的数据
            else:
                result = self._model.usr_search(p_cond)

        except Exception:
            self._logger.error("Search widget_def error, input: %s" % p_cond)
            raise OrcApiModelFailException

        return result

    def bus_delete(self, p_id):
        """
        删除单一步骤
        :param p_id:
        :return:
        """
        try:
            # 查找 widget_det_list
            widget_det_list = self.__bus_widget_det.bus_list_search(dict(widget_id=p_id))

            # 获取 widget_det_id_list
            widget_det_id_list = [widget_det.id for widget_det in widget_det_list]

            # 删除 widget_dets
            self.__bus_widget_det.bus_list_delete(widget_det_id_list)

            # 删除 widget_def
            self._model.usr_delete(p_id)

        except Exception:
            self._logger.error("Delete widget_def error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True


class WidgetDetBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "widget_det", WidgetDetMod)

    def bus_up(self, p_id):
        """
        步骤上移
        :param p_id:
        :return:
        """
        # 查询步骤信息
        widget_info = self._model.mod_search(dict(id=p_id))

        if not widget_info:
            return False

        widget_info = widget_info[0]
        widget_order = widget_info.widget_order
        pre_widget_order = int(widget_order) - 1

        # 查找最小值
        widgets = self._model.mod_search(dict(widget_id=widget_info.widget_id))
        min_order = min([widget.widget_order for widget in widgets])

        if widget_order == min_order:
            return False, u"已经是第一个步骤"

        # 查找上一个步骤
        pre_widget = self._model.mod_search(
            dict(widget_id=widget_info.widget_id, widget_order=pre_widget_order))

        # 互换位置
        if pre_widget:
            pre_widget = pre_widget[0]
            self._model.usr_update(dict(id=pre_widget.id, widget_order=widget_order))

        try:
            self._model.usr_update(dict(id=widget_info.id, widget_order=pre_widget_order))
        except AttributeError:
            return False

        return True

    def bus_down(self, p_id):
        """
        步骤下移
        :param p_id:
        :return:
        """
        # 查询步骤信息
        widget_info = self._model.mod_search(dict(id=p_id))

        if not widget_info:
            return False

        widget_info = widget_info[0]
        widget_order = widget_info.widget_order
        next_widget_order = int(widget_order) + 1

        # 查找最小值
        widgets = self._model.mod_search(dict(widget_id=widget_info.widget_id))
        max_order = max([widget.widget_order for widget in widgets])

        if widget_order == max_order:
            return False, u"已经是最后一个步骤了"

        # 查找上一个步骤
        next_widget = self._model.mod_search(
            dict(widget_id=widget_info.widget_id, widget_order=next_widget_order))

        # 互换位置
        if next_widget:
            next_widget = next_widget[0]
            self._model.usr_update(dict(id=next_widget.id, widget_order=widget_order))

        try:
            self._model.usr_update(dict(id=widget_info.id, widget_order=next_widget_order))
        except AttributeError:
            return False

        return True
