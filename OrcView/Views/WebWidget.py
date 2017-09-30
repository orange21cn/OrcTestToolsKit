# coding=utf-8
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibBaseWidget import OrcSelectBase
from OrcView.Lib.LibBaseWidget import OrcDisplay


class ObjectSelect(OrcSelectBase):

    def __init__(self, parent=None, p_mode=None, p_empty=None):
        """
        对象类型,页面/窗口/控件
        :param p_mode: 检查项时无页面
        :return:
        """
        super(ObjectSelect, self).__init__(parent, p_empty)

        self.__resource = OrcResource('Dict')

        dict_data = self.__resource.get(
            parameter=dict(dict_flag='operate_object_type'))

        if not ResourceCheck.result_status(dict_data, u'获取字典信息'):
            dict_result = list()
        else:
            dict_result = dict_data.data

        if p_mode is None:
            _data = [dict(name=_item['dict_value'], text=_item['dict_text'])
                     for _item in dict_result]
        else:
            _data = [dict(name=_item['dict_value'], text=_item['dict_text'])
                     for _item in dict_result
                     if p_mode in (() if not _item['dict_param'] else eval(_item['dict_param']))]

        self._set_item_data(_data)


class TypeSelect(OrcSelectBase):

    def __init__(self, parent=None, p_empty=None):

        super(TypeSelect, self).__init__(parent, p_empty)

        self.__resource = OrcResource('Dict')

        dict_data = self.__resource.get(
            parameter=dict(TYPE='widget_type', DATA=dict()))

        if not ResourceCheck.result_status(dict_data, u'获取字典信息'):
            dict_result = list()
        else:
            dict_result = dict_data.data

        _data = [dict(name=_item['type_name'], text=_item['type_text'])
                 for _item in dict_result]

        self._set_item_data(_data)


class OperationSelect(OrcSelectBase):

    def __init__(self, parent=None, p_empty=False):

        super(OperationSelect, self).__init__(parent, p_empty)

        self.__resource = OrcResource('Dict')

        # 控件类型
        self._type = ''

        # 使用场景,测试/检查/操作
        self._sense = 'DEBUG'

        # 数据
        self._data = list()

    def set_type(self, p_type):
        """
        设置控件类型
        :param p_type:
        :return:
        """
        self._type = p_type

        # 查询条件
        if self._type in ('BLOCK', 'PAGE', 'WINDOW', 'ALERT', 'GROUP', 'MULTI'):
            cond = dict(type_name=self._type)
        else:
            cond = dict(type_name=['BLOCK', self._type])

        # 查询数据
        dict_data = self.__resource.get(
            parameter=dict(TYPE='widget_operation', DATA=cond))

        if not ResourceCheck.result_status(dict_data, u'获取字典信息'):
            self._data = list()
        else:
            self._data = dict_data.data

        self.__reset()

    def set_sense(self, p_sense):
        """
        设置使用场景
        :param p_sense:
        :return:
        """
        self._sense = p_sense
        self.__reset()

    def __reset(self):
        """
        查询数据
        :return:
        """
        self.clear()

        # 下拉数据
        if 'CHECK' == self._sense:
            _data = [dict(name=_item['ope_name'], text=_item['check_text'])
                     for _item in self._data if _item['check_text']]
        elif 'OPERATE' == self._sense:
            _data = [dict(name=_item['ope_name'], text=_item['operate_text'])
                     for _item in self._data if _item['operate_text']]
        else:
            _data = [dict(name=_item['ope_name'], text=_item['ope_text'])
                     for _item in self._data]

        self._set_item_data(_data)


class OperationDisp(OrcDisplay):
    """
    Item operation 显示为文字
    """
    sig_operate = OrcSignal()

    def __init__(self, parent=None):

        super(OperationDisp, self).__init__(parent)

        self._type = 'CHECK'

        self.clicked.connect(self.sig_operate.emit)

    def set_type(self, p_type):
        """

        :param p_type:
        :return:
        """
        self._type = p_type

    def set_data(self, p_cmd):
        """
        设置数据
        :param p_cmd:
        :return:
        """
        if p_cmd is None:
            return

        super(OperationDisp, self).set_data([p_cmd.get_cmd_dict(),
                                             p_cmd.get_disp_text()])
