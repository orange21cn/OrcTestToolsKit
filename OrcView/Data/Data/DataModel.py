# coding=utf-8
import json

from OrcLib import LibCommon
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibProcess import get_mark
from OrcLib.LibProcess import get_widget_mark

from OrcView.Lib.LibMain import LogClient
from OrcView.Lib.LibTable import ModelTable
from OrcView.Lib.LibControl import ControlBase


class DataControl(ControlBase):

    def __init__(self):

        ControlBase.__init__(self, 'Data')


class DataModel(ModelTable):

    def __init__(self):

        ModelTable.__init__(self, 'Data')

        self.__logger = LogClient()

        self.__resource_data = OrcResource('Data')
        self.__resource_batch = OrcResource("BatchDef")
        self.__resource_case_def = OrcResource("CaseDef")
        self.__resource_case_det = OrcResource("CaseDet")
        self.__resource_step_def = OrcResource("StepDef")
        self.__resource_step_det = OrcResource("StepDet")
        self.__resource_item = OrcResource("Item")
        self.__resource_widget = OrcResource("WidgetDef")

    def service_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        data = p_data
        if 'SQL' == data['data_mode']:
            data['data_value'] = json.dumps(dict(SRC=data['data_src_type'], VALUE=data['data_value']))

        result = self.__resource_data.post(parameter=data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"增加数据", self.__logger):
            return dict()

        # 打印成功信息
        ResourceCheck.result_success(u"增加数据", self.__logger)

        return dict(id=result.data["id"])

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        result = self.__resource_data.delete(parameter=p_list)

        # 检查结果
        if not ResourceCheck.result_status(result, u"删除数据", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"删除数据", self.__logger)

        return result.status

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        result = self.__resource_data.put(path=p_data["id"], parameter=p_data)

        # 检查结果
        if not ResourceCheck.result_status(result, u"更新数据", self.__logger):
            return False

        # 打印成功信息
        ResourceCheck.result_success(u"更新数据", self.__logger)

        return result.status

    def service_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        page = LibCommon.dict_value(p_cond, "page")
        number = LibCommon.dict_value(p_cond, "page")

        # 查询 data 数据
        data_list = self.__resource_data.get(parameter=p_cond)

        # 检查结果
        if not ResourceCheck.result_status(data_list, u"查询数据", self.__logger):
            return list()

        if (page is not None) and (number is not None):
            res_data = data_list.data['data']
        else:
            res_data = data_list.data

        # 查询数据源数据
        for _item in res_data:

            # 增加数据标识显示
            _item['src_id_text'] = get_mark(_item['src_type'], _item['src_id'])

            # 增加控件标识显示
            _item['data_flag_text'] = get_widget_mark(_item['data_flag'])

        # 打印成功信息
        ResourceCheck.result_success(u"查询数据", self.__logger)

        return data_list.data
