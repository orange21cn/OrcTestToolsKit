# coding=utf-8
from OrcLib.LibApi import OrcBus
from OrcLib.LibException import OrcApiModelFailException

from PageDefMod import PageDefMod
from PageDetMod import PageDetMod


class PageDefBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "page_def", PageDefMod)

        self.__bus_page_det = PageDetBus()

    def bus_delete(self, p_id):
        """
        删除单一步骤
        :param p_id:
        :return:
        """
        try:
            # 查找 page_det_list
            page_det_list = self.__bus_page_det.bus_list_search(dict(page_id=p_id))

            # 获取 page_det_id_list
            page_det_id_list = [page_det.id for page_det in page_det_list]

            # 删除 page_dets
            self.__bus_page_det.bus_list_delete(page_det_id_list)

            # 删除 page_def
            self._model.usr_delete(p_id)

        except Exception:
            self._logger.error("Add case error, input: %s" % p_id)
            raise OrcApiModelFailException

        return True


class PageDetBus(OrcBus):

    def __init__(self):

        OrcBus.__init__(self, "page_det", PageDetMod)
