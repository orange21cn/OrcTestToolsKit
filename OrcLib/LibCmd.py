# coding=utf-8
from OrcLib.LibProgram import OrcFactory
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck


class OrcCmd(object):
    """
    命令结构类
    """
    def __init__(self, p_cmd=None):

        object.__init__(self)

        _cmd = OrcFactory.create_dict(p_cmd)

        self.__resource_page = OrcResource('PageDef')
        self.__resource_window = OrcResource('WindowDef')
        self.__resource_widget = OrcResource('WidgetDef')

        # 驱动类型,WEB/IOS...
        self.driver_type = _cmd.value('DTYPE')

        # 操作模式,操作项/检查项
        self.operate_mode = _cmd.value('MODE')

        # 对象类型,PAGE/WINDOW/WIDGET
        self.cmd_type = _cmd.value('TYPE')

        # 对象 ＩＤ
        self.cmd_object = _cmd.value('OBJECT')

        # 操作方法
        self.cmd_operation = _cmd.value('OPERATION')

        # 所需数据
        self.data = _cmd.value('DATA')

        # 对象数据
        self._object_info = self.__get_info(self.cmd_object)

    def is_web_cmd(self):
        """
        命令类型,是否 WEB
        :return:
        """
        return 'WEB' == self.driver_type

    def is_operation_mode(self):
        """
        命令模式,是否操作项
        :return:
        """
        return 'OPERATE' == self.operate_mode

    def is_check_mode(self):
        """
        命令模式,是否检查项
        :return:
        """
        return 'CHECK' == self.operate_mode

    def is_page(self):
        """
        对象类型,是否页面
        :return:
        """
        print self.cmd_type
        return 'PAGE' == self.cmd_type

    def is_window(self):
        """
        对象类型,是否窗口
        :return:
        """
        return 'WINDOW' == self.cmd_type

    def is_widget(self):
        """
        对象类型,是否控件
        :return:
        """
        return 'WIDGET' == self.cmd_type

    def is_group_widget(self):
        """
        控件类型,是否 group
        :return:
        """
        return 'GROUP' == self.cmd_object['widget_type']

    def is_frame_widget(self):
        """
        控件类型,是否 frame
        :return:
        """
        return 'FRAME' == self.cmd_object['widget_type']

    def is_block_widget(self):
        """
        控件类型,是否通用控件
        :return:
        """
        return 'BLOCK' == self._object_info['widget_type']

    def is_block_type_widget(self):
        """
        控件类型,是否基于通用控件的控件
        :return:
        """
        return self._object_info['widget_type'] in ('BLOCK', 'INP', 'BTN', 'LINK', 'SELECT')

    def is_input_widget(self):
        """
        控件类型,是否输入框
        :return:
        """
        return 'INP' == self._object_info['widget_type']

    def is_select_widget(self):
        """
        控件类型,是否下拉框
        :return:
        """
        return 'SELECT' == self._object_info['widget_type']

    def is_alert_widget(self):
        """
        控件类型,是否弹出框
        :return:
        """
        return 'ALERT' == self._object_info['widget_type']

    def get_data_num(self):
        """
        获取数据数量
        :return:
        """
        if self.is_check_mode():
            if self.cmd_operation in ('GET_TEXT', 'TEXT', 'LABEL', 'VALUE'):
                self.data = 1
            elif self.cmd_operation in ('GET_ATTR',):
                self.data = 2
            else:
                pass

        elif self.is_operation_mode():
            if self.cmd_operation in ('INPUT',):
                self.data = 1
        else:
            pass

    def set_driver_type(self, p_type):
        """
        驱动类型
        :param p_type:
        :return:
        """
        self.driver_type = p_type

    def set_operate_mode(self, p_mode):
        """
        设置操作模式,操作项/检查项
        :param p_mode:
        :return:
        """
        self.operate_mode = p_mode

    def set_cmd_type(self, p_cmd_type):
        """
        设置命令类型,page/widget
        :param p_cmd_type:
        :return:
        """
        self.cmd_type = p_cmd_type

    def set_cmd_object(self, p_cmd_object):
        """
        设置命令对象
        :param p_cmd_object:
        :return:
        """
        self.cmd_object = p_cmd_object

        self.__get_info(self.cmd_object)

    def set_cmd_operation(self, p_cmd_operation):
        """
        设置命令操作
        :param p_cmd_operation:
        :return:
        """
        self.cmd_operation = p_cmd_operation

    def set_data(self, p_data):
        """
        设置数据,非 None 表示有数据,调试模式下为实际数据,正式情况下仅代表有数据
        :param p_data:
        :return:
        """
        self.data = p_data

    def set_cmd(self, p_cmd):
        """
        设置命令
        :param p_cmd:
        :return:
        """
        self.cmd_type = p_cmd['TYPE']
        self.cmd_object = p_cmd['OBJECT']
        self.cmd_operation = p_cmd['OPERATION']

    def set_page_info(self, p_info):
        """
        设置页面信息
        :param p_info:
        :return:
        """
        self._object_info = p_info
        self.set_cmd_object(self._object_info['id'])
        self.set_cmd_type('PAGE')

    def set_widget_info(self, p_info):
        """
        设置控件信息
        :param p_info:
        :return:
        """
        self._object_info = p_info
        self.set_cmd_object(self._object_info['id'])
        self.set_cmd_type('WIDGET')

    def get_flag(self):
        """
        获取对象标识
        :return:
        """
        if self.is_web_cmd():

            if self.is_page():
                return self._object_info['page_flag']
            elif self.is_widget():
                print "ljljlj", self._object_info
                return self._object_info['widget_path']
            elif self.is_window():
                return ''
            else:
                return ''

        else:
            return ''

    def get_dict(self):
        """
        获取完整命令字典,含驱动类型和模式
        :return:
        """
        res_dict = dict(
            DTYPE=self.driver_type,
            MODE=self.operate_mode,
            TYPE=self.cmd_type,
            OBJECT=self.cmd_object,
            OPERATION=self.cmd_operation
        )

        if self.data is not None:
            res_dict['DATA'] = self.data

        return res_dict

    def get_cmd_dict(self):
        """
        获取 operation 字典
        :return:
        """
        res_dict = dict(
            TYPE=self.cmd_type,
            OBJECT=self.cmd_object,
            OPERATION=self.cmd_operation
        )

        if self.data is not None:
            res_dict['DATA'] = self.data

        return res_dict

    def __get_info(self, p_id):
        """
        获取对象信息
        :return:
        """
        if p_id is None:
            return dict()

        if self.is_page():
            result = self.__resource_page.get(path=p_id)

            if not ResourceCheck.result_status(result, '获取页面信息'):
                return dict()

            return result.data

        elif self.is_widget():

            result = self.__resource_widget.get(path=p_id)

            if not ResourceCheck.result_status(result, '获取控件信息'):
                return None

            return result.data
        else:
            pass

    @staticmethod
    def static_get_disp_text(p_cmd):
        """
        获取检查项显示文字,静态函数
        :param p_cmd:
        :return:
        """
        cmd = OrcCmd(p_cmd)
        return cmd.get_disp_text()

    def get_disp_text(self):
        """
        获取检查项显示文字
        :return:
        """
        def get_operation_text():
            """
            获取操作数据
            :return:
            """
            resource_dict = OrcResource('Dict')

            res_operation = resource_dict.get(
                parameter=dict(TYPE='widget_operation', DATA=dict(ope_name=self.cmd_operation)))

            if not ResourceCheck.result_status(res_operation, u'获取字典数据'):
                return ''

            if not res_operation.data:
                return ''

            if self.is_check_mode():
                return res_operation.data[0]['check_text']
            elif self.is_operation_mode():
                return res_operation.data[0]['operate_text']
            else:
                return res_operation.data[0]['ope_text']

        if self.is_web_cmd():

            # 页面命令
            if self.is_page():
                res_text = u"页面[%s].%s" % (self.get_flag(), get_operation_text())

            # 控件命令
            elif self.is_widget():
                res_text = u"控件[%s].%s" % (self.get_flag(), get_operation_text())

            # 其他
            else:
                res_text = ''

            if self.data is not None:
                res_text = u"%s 数据 %s" % (res_text, self.data)

            return res_text
        else:
            # 暂时没用,用于兼容其他类型的驱动
            # object_text = ''
            # operation_text = ''
            pass
