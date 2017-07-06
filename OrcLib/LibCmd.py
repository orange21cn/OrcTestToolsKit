# coding=utf-8
from OrcLib.LibProgram import OrcFactory
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibType import WebObjectType
from OrcLib.LibType import WebItemModeType
from OrcLib.LibType import WebDriverType


class OrcCmd(object):
    """
    用于驱动执行的命令,包括一些系统命令,基本格工是: {TYPE, CMD}, 格式为dict 可以生成或者读取
    {TYPE: type, CMD: cmd}
    """
    def __init__(self, p_cmd=None):

        object.__init__(self)

        _cmd = OrcFactory.create_dict(p_cmd)

        # 命令类型
        self.type = None

        # 命令
        self.cmd = None

        # 初始化数据
        self.set_type(_cmd.value('TYPE'))
        self.set_cmd(_cmd.value('CMD'))

    def set_type(self, p_type):
        """
        设置类型
        :param p_type:
        :return:
        """
        if p_type in ('SYSTEM', 'DRIVER'):
            self.type = p_type

    def set_sys_type(self):
        """
        设置为系统类型
        :return:
        """
        self.type = "SYSTEM"

    def is_system(self):
        """
        是系统命令
        :return:
        """
        return 'SYSTEM' == self.type

    def set_driver_type(self, p_type):
        """
        设置为驱动类型
        :param p_type:
        :return:
        """
        self.type = 'DRIVER'

    def is_driver(self):
        """
        是驱动命令
        :return:
        """
        return 'DRIVER' == self.type

    def set_cmd(self, p_cmd):
        """
        设置命令
        :param p_cmd:
        :return:
        """
        if self.is_system():
            self.cmd = OrcSysCmd(p_cmd)
        elif self.is_driver():
            self.cmd = OrcDriverCmd(p_cmd)
        else:
            self.cmd = None


class OrcSysCmd(object):
    """
    系统命令, 暂时只有 quit, {OPERATION: operation, DATA: data}
    """
    def __init__(self, p_cmd=None):

        object.__init__(self)

        # 操作
        self.operation = None

        # 初始化数据
        self.set_cmd(p_cmd)

    def set_cmd(self, p_cmd):
        """
        设置命令
        :param p_cmd:
        :return:
        """
        _cmd = OrcFactory.create_dict(p_cmd)

        self.set_operation(_cmd.value('OPERATION'))

    def set_operation(self, p_operation):
        """
        设置操作
        :param p_operation:
        :return:
        """
        if p_operation in ('OPERATION',):
            self.operation = p_operation

    def set_quit(self):
        """
        设置为退出
        :return:
        """
        self.operation = 'QUIT'

    def is_quit(self):
        """
        是否退出
        :return:
        """
        return 'QUIT' == self.operation


class OrcDriverCmd(object):
    """

    """
    def __init__(self, p_cmd=None):

        object.__init__(self)

        # 驱动类型,WEB/IOS...
        self.driver_type = None

        # 操作模式,操作项/检查项
        self.operate_mode = None

        # 命令
        self.cmd = None

        # 初始化数据

        if p_cmd is not None:

            _cmd = OrcFactory.create_dict(p_cmd)

            self.set_type(_cmd.value('DTYPE'))
            self.set_mode(_cmd.value('MODE'))
            self.set_cmd(_cmd.value('CMD'))

    def set_type(self, p_type):
        """

        :param p_type:
        :return:
        """
        if p_type in WebDriverType.all():
            self.driver_type = p_type

    def set_web(self):
        """

        :return:
        """
        self.driver_type = WebDriverType.WEB

    def is_web(self):
        """

        :return:
        """
        return WebDriverType.WEB == self.driver_type

    def set_mode(self, p_mode):
        """

        :param p_mode:
        :return:
        """
        if p_mode in WebItemModeType.all():
            self.operate_mode = p_mode
            if self.cmd is not None:
                self.cmd.set_mode(p_mode)

    def set_operation(self):
        """

        :return:
        """
        self.operate_mode = WebItemModeType.OPERATE

    def is_operation(self):
        """

        :return:
        """
        return WebItemModeType.OPERATE == self.operate_mode

    def set_check(self):
        """

        :return:
        """
        self.operate_mode = WebItemModeType.CHECK

    def is_check(self):
        """

        :return:
        """
        return WebItemModeType.CHECK == self.operate_mode

    def set_cmd(self, p_cmd):
        """

        :param p_cmd:
        :return:
        """
        assert isinstance(p_cmd, dict)

        if self.is_web():
            self.cmd = WebCmd(p_cmd)
            self.cmd.set_mode(self.operate_mode)

    def get_disp_text(self):
        """

        :return:
        """
        return self.cmd.get_disp_text()


class WebCmd(object):
    """
    命令结构类
    """
    def __init__(self, p_cmd=None):

        object.__init__(self)

        self.__resource_page = OrcResource('PageDef')
        self.__resource_window = OrcResource('WindowDef')
        self.__resource_widget = OrcResource('WidgetDef')

        # 模式,操作项/检查项,由外部提供
        self.mode = None

        _cmd = OrcFactory.create_dict(p_cmd)

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

    def set_mode(self, p_mode):
        """
        设置模式
        :param p_mode:
        :type p_mode: WebItemModeType
        :return:
        """
        self.mode = p_mode

        self.__cal_data()

    def set_cmd_type(self, p_type):
        """

        :param p_type:
        :return:
        """
        if p_type in WebObjectType.all():
            self.cmd_type = p_type

    def set_page(self):
        """

        :return:
        """
        self.cmd_type = WebObjectType.PAGE

    def is_page(self):
        """
        对象类型,是否页面
        :return:
        """
        return WebObjectType.PAGE == self.cmd_type

    def set_window(self):
        """

        :return:
        """
        self.cmd_type = WebObjectType.WINDOW

    def is_window(self):
        """
        对象类型,是否窗口
        :return:
        """
        return WebObjectType.WINDOW == self.cmd_type

    def set_widget(self):
        """

        :return:
        """
        self.cmd_type = WebObjectType.WIDGET

    def is_widget(self):
        """
        对象类型,是否控件
        :return:
        """
        return WebObjectType.WIDGET == self.cmd_type

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

        self.__cal_data()

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
        self.set_cmd_type(WebObjectType.PAGE)

    def set_widget_info(self, p_info):
        """
        设置控件信息
        :param p_info:
        :return:
        """
        self._object_info = p_info
        self.set_cmd_object(self._object_info['id'])
        self.set_cmd_type(WebObjectType.WIDGET)

    def get_flag(self):
        """
        获取对象标识
        :return:
        """
        if self._object_info is None:
            return ''

        if self.is_page():
            return self._object_info['page_flag']
        elif self.is_widget():
            return self._object_info['widget_path']
        elif self.is_window():
            return ''
        else:
            return ''

    def get_widget_type(self):
        """

        :return:
        """
        if self.is_page():
            return None

        return self._object_info['widget_type']

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

    def get_disp_text(self):
        """
        获取检查项显示文字
        :param p_type:
        :type p_type: WebItemModeType
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

            if WebItemModeType.CHECK == self.mode:
                return res_operation.data[0]['check_text']
            elif WebItemModeType.OPERATE == self.mode:
                return res_operation.data[0]['operate_text']
            else:
                return ''

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
            res_text = u"%s.数据(%s)" % (res_text, self.data)

        return res_text

    def __cal_data(self):
        """
        计算数据数量
        :return:
        """
        if WebItemModeType.OPERATE == self.mode:
            if self.cmd_operation in ('INPUT',):
                self.data = 1

        elif WebItemModeType.CHECK == self.mode:
            if self.cmd_operation in ('GET_TEXT', 'TEXT', 'LABEL', 'VALUE'):
                self.data = 1
            elif self.cmd_operation in ('GET_ATTR',):
                self.data = 2
            else:
                pass
        else:
            pass
