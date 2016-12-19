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
