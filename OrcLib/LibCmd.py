# coding=utf-8
from OrcLib.LibProgram import OrcFactory
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibType import WebObjectType
from OrcLib.LibType import WebItemModeType
from OrcLib.LibType import DriverType
from OrcLib.LibType import BatchType
from OrcLib.LibType import CaseType
from OrcLib.LibType import StepType
from OrcLib.LibType import ItemType
from OrcLib.LibType import DataScopeType
from OrcLib.LibStatus import RecordStatus
from OrcLib.LibDatabase import TabBatchDef
from OrcLib.LibDatabase import TabCaseDef
from OrcLib.LibDatabase import TabStepDef
from OrcLib.LibDatabase import TabItem
from OrcLib.LibCommon import OrcString
from OrcLib.LibProcess import get_page_def_mark
from OrcLib.LibProcess import get_widget_mark


class OrcCmd(object):
    """
    用于驱动执行的命令,包括一些系统命令,基本格工是: {TYPE, CMD}, 格式为dict 可以生成或者读取
    {TYPE: type, CMD: cmd}
    """
    def __init__(self, p_cmd=None):

        object.__init__(self)

        # 命令类型
        self.type = None

        # 命令
        self.cmd = None

        # session
        self.session = None

        # 初始化数据
        _cmd = OrcFactory.create_default_dict(p_cmd)

        self.set_type(_cmd.value('TYPE'))
        self.set_cmd(_cmd.value('CMD'))
        self.set_session(_cmd.value('SESSION'))

    def set_session(self, p_session):
        """
        设置 session
        :param p_session:
        :return:
        """
        self.session = p_session

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

    def set_driver_type(self):
        """
        设置为驱动类型
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
        # 系统命令类型
        if isinstance(p_cmd, OrcSysCmd):
            self.cmd = p_cmd
            self.set_sys_type()

        # 驱动命令类型
        elif isinstance(p_cmd, OrcDriverCmd):
            self.cmd = p_cmd
            self.set_driver_type()

        # 字典直接设置
        elif isinstance(p_cmd, dict):

            # 设置为系统命令
            if self.is_system():
                self.cmd = OrcSysCmd(p_cmd)

            # 设置为驱动命令
            elif self.is_driver():
                self.cmd = OrcDriverCmd(p_cmd)

            # 未知不处理
            else:
                self.cmd = None
        else:
            pass

    def get_cmd_dict(self):
        """
        获取命令字典
        :return:
        """
        return dict(
            TYPE=self.type,
            SESSION=self.session,
            CMD=self.cmd.get_cmd_dict()
        )


class OrcSysCmd(object):
    """
    系统命令, 暂时只有 quit, {OPERATION: operation, DATA: data}
    """
    def __init__(self, p_cmd=None):

        object.__init__(self)

        # 操作
        self._operation = None

        # 数据
        self._data = None

        # 初始化数据
        self.set_cmd(p_cmd)

    def set_cmd(self, p_cmd):
        """
        设置命令
        :param p_cmd:
        :return:
        """
        _cmd = OrcFactory.create_default_dict(p_cmd)

        self.set_operation(_cmd.value('OPERATION'))

    def set_operation(self, p_operation):
        """
        设置操作
        :param p_operation:
        :return:
        """
        if p_operation in ('ENV', 'QUIT', 'OCCUPY', 'RELEASE'):
            self._operation = p_operation

    def set_quit(self):
        """
        设置为退出
        :return:
        """
        self._operation = 'QUIT'

    def is_quit(self):
        """
        是否退出
        :return:
        """
        return 'QUIT' == self._operation

    def set_occupy(self):
        """
        占用
        :return:
        """
        self._operation = 'OCCUPY'

    def is_occupy(self):
        """
        是否占用
        :return:
        """
        return 'OCCUPY' == self._operation

    def set_release(self):
        """
        释放
        :return:
        """
        self._operation = 'RELEASE'

    def is_release(self):
        """
        是否是释放
        :return:
        """
        return 'RELEASE' == self._operation

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        self._data = p_data

    def get_data(self):
        """
        获取数据
        :return:
        """
        return self._data

    def set_parameter(self):
        """
        设置环境
        :return:
        """
        self._operation = 'PARAMETER'

    def is_parameter(self):
        """
        是否设置环境
        :return:
        """
        return 'PARAMETER' == self._operation

    def get_cmd_dict(self):
        """
        获取命令字典
        :return:
        """
        return dict(
            OPERATION=self._operation,
            DATA=self._data
        )


class DataCmd(object):

    def __init__(self, p_cmd=None):

        object.__init__(self)

        # 数据标识
        self.cmd_object = OrcString.get_long_str()

        # 数据个数
        self.data = None

        # 模式 operate/check
        self.mode = None

        # 初始化数据
        if p_cmd is not None:

            _cmd = OrcFactory.create_default_dict(p_cmd)

            self.set_object(_cmd.value('OBJECT'))
            self.set_data(_cmd.value('DATA'))

    def set_object(self, p_object):
        """
        设置对象标识
        :param p_object:
        :return:
        """
        self.cmd_object = p_object

    def set_data(self, p_data):
        """
        设置数据个数
        :param p_data:
        :return:
        """
        self.data = p_data

    def set_mode(self, operate_mode):
        """
        设置操作模式,非命令本身字段,用于计算data数
        :param operate_mode:
        :return:
        """
        self.mode = operate_mode

        self.__cal_data()

    def set_cmd(self, p_data):
        """
        设置命令
        :param p_data:
        :return:
        """
        data = OrcFactory.create_default_dict(p_data)
        self.cmd_object = data.value('OBJECT')
        self.data = data.value('DATA')

    def get_cmd_dict(self):
        """
        获取命令字典
        :return:
        """
        return dict(
            OBJECT=self.cmd_object,
            DATA=self.data
        )

    def get_disp_text(self):
        """
        获取显示文字
        :return:
        """
        if self.cmd_object is None:
            return ''

        return u"数据操作[%s].数据(%s)" % (self.cmd_object, self.data)

    def __cal_data(self):
        """
        计算 data 的数量
        :return:
        """
        if WebItemModeType.OPERATE == self.mode:
            self.data = 1
        elif WebItemModeType.CHECK == self.mode:
            self.data = 2
        else:
            pass


class OrcDriverCmd(object):
    """
    驱动命令
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

            _cmd = OrcFactory.create_default_dict(p_cmd)

            self.set_type(_cmd.value('DTYPE'))
            self.set_mode(_cmd.value('MODE'))
            self.set_cmd(_cmd.value('CMD'))

    def set_type(self, p_type):
        """

        :param p_type:
        :return:
        """
        if p_type in DriverType.all():
            self.driver_type = p_type

    def set_web(self):
        """

        :return:
        """
        self.driver_type = DriverType.WEB

    def is_web(self):
        """

        :return:
        """
        return DriverType.WEB == self.driver_type

    def set_data(self):
        """
        设置为 sql 类型
        :return:
        """
        self.driver_type = 'DATA'

    def is_data(self):
        """
        是否 SQL
        :return:
        """
        return 'DATA' == self.driver_type

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
        设置命令
        :param p_cmd:
        :return:
        """
        if isinstance(p_cmd, WebCmd):
            self.cmd = p_cmd
            self.set_web()

        # 设置为 data 类型
        elif isinstance(p_cmd, DataCmd):
            self.cmd = p_cmd
            self.set_data()

        elif isinstance(p_cmd, dict):

            if self.is_web():
                self.cmd = WebCmd(p_cmd)
            elif self.is_data():
                self.cmd = DataCmd(p_cmd)
            else:
                pass

        else:
            pass

        if self.cmd is not None:
            self.cmd.set_mode(self.operate_mode)

    def get_cmd_dict(self):
        """

        :return:
        """
        return dict(
            DTYPE=self.driver_type,
            MODE=self.operate_mode,
            CMD=self.cmd.get_cmd_dict()
        )

    def get_disp_text(self):
        """

        :return:
        """
        if self.cmd is not None:
            return self.cmd.get_disp_text()
        else:
            return ''


class WebCmd(object):
    """
    命令结构类
    """
    def __init__(self, p_cmd=None):

        object.__init__(self)

        # 资源
        self.__resource_page = OrcResource('PageDef')
        self.__resource_window = OrcResource('WindowDef')
        self.__resource_widget = OrcResource('WidgetDef')

        # 模式,操作项/检查项,由外部提供
        self.mode = None

        # 对象类型,PAGE/WINDOW/WIDGET
        self.cmd_type = None

        # 对象 ＩＤ, 兼容多控件操作
        self.cmd_object_ids = dict(FROM=None, TO=None)

        # 操作方法
        self.cmd_operation = None

        # 所需数据
        self.data_num = None

        # 输入数据
        self.data_inp = None

        # 对比数据
        self.data_chk = None

        # 对象数据
        self._object_info = dict(FROM=OrcFactory.create_default_dict(),
                                 TO=OrcFactory.create_default_dict())

        self.set_cmd(p_cmd)

    @property
    def cmd_object(self):
        return self.cmd_object_ids['FROM']

    @cmd_object.setter
    def cmd_object(self, p_id):
        self.cmd_object_ids['FROM'] = p_id
        # self._object_info[0] = self.__get_info(p_id)

    @property
    def cmd_object_to(self):
        return self.cmd_object_ids['TO']

    @cmd_object_to.setter
    def cmd_object_to(self, p_id):
        self.cmd_object_ids['TO'] = p_id
        # self._object_info['TO'] = self.__get_info(p_id)

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
        设置命令类型
        :param p_type:
        :return:
        """
        print ">>>>>>>", p_type
        if p_type in WebObjectType.all():
            self.cmd_type = p_type

    def set_page(self):
        """
        设置为页面
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
        设置为窗口
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
        设置为控件
        :return:
        """
        self.cmd_type = WebObjectType.WIDGET

    def is_widget(self):
        """
        对象类型,是否控件
        :return:
        """
        return WebObjectType.WIDGET == self.cmd_type

    def set_driver(self):
        """
        设置为驱动
        :return:
        """
        self.cmd_type = WebObjectType.DRIVER

    def is_driver(self):
        """
        对象类型,是否驱动
        :return:
        """
        return WebObjectType.DRIVER == self.cmd_type

    def set_cmd_object(self, p_cmd_object, p_src=None):
        """
        设置命令对象
        :param p_src:
        :param p_cmd_object:
        :return:
        """
        _src = p_src or 'FROM'

        if 'FROM' == _src:
            self.cmd_object = p_cmd_object
        elif 'TO' == _src:
            self.cmd_object_to = p_cmd_object
        else:
            pass

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
        :type p_data: list
        :return:
        """
        if len(p_data) != self.data_num:
            pass

        if self.data_inp:
            self.data_inp = p_data[:int(self.data_inp)]

        if self.data_chk:
            self.data_chk = p_data[- int(self.data_chk):]

    def set_cmd(self, p_cmd):
        """
        设置命令
        :param p_cmd:
        :return:
        """
        _cmd = OrcFactory.create_default_dict(p_cmd)
        _cmd_object = str(_cmd.value('OBJECT'))
        if _cmd_object:
            _cmd_object = _cmd_object.split('|')
        else:
            _cmd_object = ['']

        self.cmd_type = _cmd.value('TYPE')
        self.cmd_object = _cmd_object[0]
        self.cmd_operation = _cmd.value('OPERATION')
        self.data_num = _cmd.value('DATA')
        self.data_inp = _cmd.value('DATA_INP')
        self.data_chk = _cmd.value('DATA_CHK')

        if 2 == len(_cmd_object):
            self.cmd_object_to = _cmd_object[0]

    def set_page_from_info(self, p_info):
        """
        设置页面信息
        :param p_info:
        :return:
        """
        self._object_info['FROM'].init(p_info)
        self.set_cmd_object(self._object_info['FROM'].value('id'))
        self.set_cmd_type(WebObjectType.PAGE)

    def set_widget_from_info(self, p_info):
        """
        设置控件信息
        :param p_info:
        :return:
        """
        self._object_info['FROM'].init(p_info)
        self.set_cmd_object(self._object_info['FROM'].value('id'))
        self.set_cmd_type(WebObjectType.WIDGET)

    def set_widget_to_info(self, p_info):
        """
        设置控件信息
        :param p_info:
        :return:
        """
        print 100, p_info
        self._object_info['TO'].init(p_info)
        self.set_cmd_object(self._object_info['TO'].value('id'), 'TO')

    def get_flag(self, p_src=None):
        """
        获取对象标识
        :param p_src:
        :return:
        """
        _src = p_src or 'FROM'

        if self.is_page():
            return self._object_info[_src].value('page_flag') or get_page_def_mark(self.cmd_object)
        elif self.is_widget():
            return self._object_info[_src].value('widget_path') or get_widget_mark(self.cmd_object)
        elif self.is_window():
            return ''
        else:
            return ''

    def get_widget_type(self, p_src=None):
        """

        :param p_src:
        :return:
        """
        _src = p_src or 'FROM'

        if self.is_page():
            return None

        return self._object_info[_src].value('widget_type')

    def get_object_info(self, p_flag, p_src=None):
        """
        获取对象原始信息
        :param p_src:
        :param p_flag:
        :return:
        """
        _src = p_src or 'FROM'

        return self._object_info[_src].value(p_flag)

    def get_cmd_dict(self):
        """
        获取 operation 字典
        :return:
        """
        print 1, self.cmd_object
        print 2, self.cmd_object_to

        _cmd_object = self.cmd_object
        if self.cmd_object_to:
            _cmd_object = "%s|%s" % (_cmd_object, self.cmd_object_to)

        res_dict = dict(
            TYPE=self.cmd_type,
            OBJECT=_cmd_object,
            OPERATION=self.cmd_operation)

        if self.data_num is not None:
            res_dict['DATA'] = self.data_num

        if self.data_inp is not None:
            res_dict['DATA_INP'] = self.data_inp

        if self.data_chk is not None:
            res_dict['DATA_CHK'] = self.data_chk

        return res_dict

    def __get_info(self, p_id):
        """
        获取对象信息
        :return:
        """
        rtn = OrcFactory.create_default_dict()

        if p_id is None:
            return rtn

        if self.is_page():
            result = self.__resource_page.get(path=p_id)

            if not ResourceCheck.result_status(result, '获取页面信息'):
                return rtn

            rtn.init(result.data)

        elif self.is_widget():

            result = self.__resource_widget.get(path=p_id)

            if not ResourceCheck.result_status(result, '获取控件信息'):
                return rtn

            rtn.init(result.data)
        else:
            pass

        return rtn

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

            if self.cmd_object_to:
                _flag = "%s|%s" % (self.get_flag(), self.get_flag('TO'))
            else:
                _flag = self.get_flag()

            res_text = u"控件[%s].%s" % (_flag, get_operation_text())

        # 其他
        else:
            res_text = ''

        if self.data_num is not None:
            res_text = u"%s.数据(%s)" % (res_text, self.data_num)

        return res_text

    def __cal_data(self):
        """
        计算数据数量
        :return:
        """
        # 已经设置过数据,不再重新计算数量
        if isinstance(self.data_inp, list) or isinstance(self.data_chk, list):
            return

        if WebItemModeType.OPERATE == self.mode:
            if self.cmd_operation in ('INPUT', 'TEXT', 'LABEL', 'VALUE', 'SCRIPT', 'DEL_ATTR'):
                self.data_num = 1
                self.data_inp = 1
            elif self.cmd_operation in ('SET_ATTR',):
                self.data_num = 1
                self.data_inp = 2
            else:
                pass

        elif WebItemModeType.CHECK == self.mode:
            if self.cmd_operation in ('GET_TEXT',):
                self.data_num = 1
                self.data_chk = 1
            elif self.cmd_operation in ('GET_ATTR',):
                self.data_num = 2
                self.data_inp = 1
                self.data_chk = 1
            else:
                pass
        else:
            pass


class OrcRecordCmd(object):
    """
    记录字符串
    """
    def __init__(self, p_cmd=None):

        """
        init, cmd str to type
        :param p_cmd:
        :return:
        """
        object.__init__(self)

        inp = OrcFactory.create_default_dict(p_cmd)

        # id
        self.id = inp.value('id')

        # parent id
        self.pid = inp.value('pid')

        # type
        self.run_det_type = inp.value('run_det_type')

        # flag
        self.flag = inp.value('flag')

        # description
        self.desc = inp.value('desc')

        # status
        self.status = RecordStatus(inp.value('status'))

    def batch(self, p_data):
        """
        batch init func, database data to type
        :param p_data:
        :return:
        """
        _data = TabBatchDef(p_data)

        self.id = _data.id
        self.pid = _data.pid
        self.run_det_type = _data.batch_type
        self.flag = _data.batch_no
        self.desc = _data.batch_desc

    def case(self, p_data, p_pid=None):
        """
        case init func, database data to type
        :param p_pid:
        :param p_data:
        :return:
        """
        _data = TabCaseDef(p_data)

        self.id = _data.id
        self.pid = _data.pid
        self.run_det_type = _data.case_type
        self.flag = _data.case_no
        self.desc = _data.case_desc

        if p_pid is not None:
            self.pid = p_pid

    def step(self, p_data, p_no, p_pid=None):
        """
        step init func, database data to type
        :param p_no:
        :param p_pid:
        :param p_data:
        :return:
        """
        _data = TabStepDef(p_data)

        self.id = _data.id
        self.run_det_type = _data.step_type
        self.flag = p_no
        self.desc = _data.step_desc

        if p_pid is not None:
            self.pid = p_pid

    def item(self, p_data, p_no=None, p_pid=None):
        """
        item init func database data to type
        :param p_pid:
        :param p_no:
        :param p_data:
        :return:
        """
        _data = TabItem(p_data)

        self.id = _data.id
        self.run_det_type = _data.item_type
        self.flag = p_no
        self.desc = _data.item_desc

        if p_pid is not None:
            self.pid = p_pid

    def is_batch_type(self):
        """
        batch type, include batch and batch suit
        :return:
        """
        return self.run_det_type in BatchType.all()

    def is_batch_suite(self):
        """
        batch suite
        :return:
        """
        return self.run_det_type == BatchType.BATCH_SUITE

    def is_batch(self):
        """
        batch
        :return:
        """
        return self.run_det_type == BatchType.BATCH

    def is_case_type(self):
        """
        case type, include case and case suite
        :return:
        """
        return self.run_det_type in CaseType.all()

    def is_cases(self):
        """
        case suit, case
        :return:
        """
        return self.run_det_type in (CaseType.CASE_SUITE, CaseType.CASE)

    def is_funcs(self):
        """
        function suit, function
        :return:
        """
        return self.run_det_type in (CaseType.FUNC_SUITE, CaseType.FUNC)

    def is_case_suite(self):
        """
        case suite
        :return:
        """
        return self.run_det_type == CaseType.CASE_SUITE

    def is_case(self):
        """
        case
        :return:
        """
        return self.run_det_type == CaseType.CASE

    def is_func_suite(self):
        """
        function suite
        :return:
        """
        return self.run_det_type == CaseType.FUNC_SUITE

    def is_func(self):
        """
        function
        :return:
        """
        return self.run_det_type == CaseType.FUNC

    def is_step_type(self):
        """
        normal step and function step
        :return:
        """
        return self.run_det_type in StepType.all()

    def is_normal_step(self):
        """
        normal step
        :return:
        """
        return self.run_det_type == StepType.STEP_NORMAL

    def is_func_step(self):
        """
        function step
        :return:
        """
        return self.run_det_type == StepType.STEP_FUNC

    def is_item_type(self):
        """
        item type, include ....
        :return:
        """
        return self.run_det_type in ItemType.all()

    def is_web_item(self):
        """
        web item
        :return:
        """
        return self.run_det_type == ItemType.WEB

    def is_data_item(self):
        """
        data item
        :return:
        """
        return self.run_det_type == ItemType.DATA

    def get_scope(self):
        """

        :return:
        """
        if self.is_batch():
            return DataScopeType.BATCH
        elif self.is_case():
            return DataScopeType.CASE
        elif self.is_step_type():
            return DataScopeType.STEP
        else:
            return DataScopeType.ITEM

    def to_dict(self):
        """
        转换为 json/dict
        :return:
        """
        return dict(
            id=self.id,
            pid=self.pid,
            run_det_type=self.run_det_type,
            flag=self.flag,
            desc=self.desc,
            status=self.status.get_status())
