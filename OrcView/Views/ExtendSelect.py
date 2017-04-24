# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibView import OrcSelectBase


class DataSrcSelect(OrcSelectBase):

    def __init__(self):

        OrcSelectBase.__init__(self)

        self.__logger = LogClient()
        self.__resource = OrcResource('DataSrc')

        result = self.__resource.get(parameter=dict())

        # 检查结果
        if not ResourceCheck.result_status(result, u"查询数据源数据", self.__logger):
            return

        dict_data = [dict(name=_item['id'], text=_item['name'])
                     for _item in result.data]

        self._set_item_data(dict_data)
