# coding=utf-8
import re
import datetime

from OrcLib.LibCmd import OrcRecordCmd
from OrcLib.LibCommon import OrcString
from OrcLib.LibProgram import OrcFactory
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from OrcLib.LibDatabase import TabData


class OrcDataClient(object):

    def __init__(self):

        object.__init__(self)

        # Log
        self._logger = OrcLog('basic.lib_data')

        # Data resource
        self._resource_data = OrcResource('Data')

        # DataBase resource
        self._resource_database = OrcResource('DataBase')

        # Step detail resource
        self._resource_step_det = OrcResource('StepDet')

        # Case detail resource
        self._resource_case_det = OrcResource('CaseDet')

        # Case resource
        self._resource_case_def = OrcResource('CaseDef')

        # 环境
        self._env = 'TEST'

    def set_env(self, p_env):
        """
        设置环境
        :param p_env:
        :return:
        """
        self._env = p_env

    def get_one_cmd_data(self, p_cmd, p_flag, p_func):
        """
        获取一个数据
        :param p_cmd:
        :param p_flag:
        :return:
        """
        data = self.get_cmd_data(p_cmd, p_flag, p_func)
        if data:
            return data[0]
        else:
            return data

    def get_cmd_data(self, p_cmd, p_flag, p_func):
        """
        获取命令数据,要考虑路径
        :param p_cmd:
        :type p_cmd: OrcRecordCmd
        :param p_flag:
        :return:
        """
        # 先获取计划数据
        # data = self._get_batch_data(p_cmd.id, p_flag)
        # if not data:
        #     return data
        if p_func is not None:
            return self._get_step_data(p_func, p_flag)

        # 普通步骤从步骤项数据开始
        if p_cmd.is_item_type():
            return self._get_item_data(p_cmd.id, p_flag)

        # 函数步骤从步骤开始
        elif p_cmd.is_step_type():
            return self._get_step_data(p_cmd.id, p_flag)

        else:
            return None

    def _get_item_data(self, p_id, p_flag):
        """
        获取步骤项数据
        :return:
        """
        data = self.get_data('ITEM', p_id, p_flag)
        if data:
            return data

        step_det_info = self._resource_step_det.get(parameter=dict(item_id=p_id))

        if not ResourceCheck.result_status(step_det_info, 'Get step det info', self._logger):
            return None

        if not step_det_info.data:
            return None

        step_id = step_det_info.data[0]['step_id']

        return self._get_step_data(step_id, p_flag)

    def _get_step_data(self, p_id, p_flag):
        """
        获取步骤数据
        :return:
        """
        data = self.get_data('STEP', p_id, p_flag)
        if data:
            return data

        case_det_info = self._resource_case_det.get(parameter=dict(step_id=p_id))

        if not ResourceCheck.result_status(case_det_info, 'Get case det info', self._logger):
            return None

        if not case_det_info.data:
            return None

        case_id = case_det_info.data[0]['case_id']

        return self._get_case_data(case_id, p_flag)

    def _get_case_data(self, p_id, p_flag):
        """
        获取用例数据
        :return:
        """
        data = self.get_data('CASE', p_id, p_flag)
        if data:
            return data

        case_path_info = self._resource_case_def.get(path=p_id)

        if not ResourceCheck.result_status(case_path_info, 'Get case info', self._logger):
            return None

        if not case_path_info.data:
            return None

        if not case_path_info.data['pid']:
            return None

        return self._get_case_data(case_path_info.data['pid'], p_flag)

    def _get_batch_data(self, p_id, p_flag):
        """
        获取计划数据
        :return:
        """
        pass

    def get_data(self, p_src_type, p_src_id, p_data_flag):
        """
        获取数据
        :param p_data_flag: 标识
        :param p_src_id: 源id
        :param p_src_type: 源类型
        :return:
        """
        # 查询数据
        result = self._resource_data.get(parameter=dict(
            test_env=self._env,
            src_id=p_src_id,
            src_type=p_src_type,
            data_flag=p_data_flag))

        if not ResourceCheck.result_status(result, u"读取数据", self._logger):
            return []

        if not result.data:
            return []

        return [self._generate_data(_data) for _data in result.data]

    def get_one(self, p_src_type, p_src_id, p_data_flag):
        """
        获取一个数据
        :param p_data_flag:
        :param p_src_id:
        :param p_src_type:
        :return:
        """
        datas = self.get_data(p_src_type, p_src_id, p_data_flag)

        if not datas:
            return ''
        else:
            return datas[0]

    def set_data(self, p_id, p_data):
        """
        设置数据
        :param p_id:
        :param p_data:
        :return:
        """
        result = self._resource_data.put(path=p_id, parameter=dict(data_value=p_data))

        if not ResourceCheck.result_status(result, u"写入数据", self._logger):
            return False

        if not result.data:
            return False

        return result.data

    def _generate_data(self, p_data):

        # 生成返回数据
        res_data = TabData(p_data)

        # 通过数据来源获取数据
        if 'DEFAULT' == res_data.data_mode:
            data_str = res_data.data_value

        # 通过文件获取数据,数据模块的库中存储文件信息
        elif 'FILE' == res_data.data_mode:
            file_path = res_data.data_value
            data_str = file_path  # Todo 需要转换

        # 数据存储在目标数据库,数据模块的库存储目标数据库信息
        elif 'DATABASE' == res_data.data_mode:
            database_desc = res_data.data_value
            data_str = self._search_sql(self._env, database_desc)

            if res_data.data_type not in ('ARRAY',):
                data_str = data_str[0][0]
        else:
            return None

        # 通过获取的原始数据生成最终归数据
        if 'STR' == res_data.data_type:
            return str(data_str)
        elif 'INT' == res_data.data_type:
            return int(data_str)
        elif 'ARRAY' == res_data.data_type:
            if isinstance(data_str, str):
                data_str = eval(data_str)
            if isinstance(data_str, list):
                return data_str
        elif 'USER_DEFINE' == res_data.data_type:
            data, template = UserDefStr.static_get_data(data_str)
            if data_str != template:
                self.set_data(res_data.id, template)
            return data
        else:
            return None

    def _search_sql(self, p_env, p_data):
        """
        根据 DATA_SRC TYPE SQL
        :param p_env:
        :param p_data: {SOURCE, SQL}
        :return:
        """
        data = p_data
        if not isinstance(data, dict):
            data = eval(data)

        data = OrcFactory.create_default_dict(data)
        data_src = "%s.%s" % (data.value('SRC'), p_env)

        sql = data.value('SQL')

        result = self._resource_database.get(parameter=dict(DATA_SRC=data_src, SQL=sql, TYPE='DATA'))

        if not ResourceCheck.result_status(result, "获取 SQL 数据 %s:%s" % (data_src, sql)):
            return None

        return result.data


class UserDefStr(object):

    def __init__(self, p_str=None):

        object.__init__(self)

        # Log
        self._logger = OrcLog('basic.lib_data.user_def_str')

        # Data resource
        self._resource_data = OrcResource('Data')

        # 原始字符串
        self._origin_str = None

        # 分解后模板列表
        self._temp_list = None

        # 分解后结果列表
        self._result_list = None

    def _split_template(self):
        """
        将模板字符串分割为数组
        :return:
        """
        reg = re.compile(r'[{}]')
        res_list = reg.split(self._origin_str)

        self._temp_list = res_list
        self._result_list = res_list[:]

    @staticmethod
    def _combine_template(p_name, p_para, p_extra=None):
        """
        结合模板串
        :param p_name:
        :param p_para:
        :param p_extra:
        :return:
        """
        if p_extra is None:
            return "{%s:%s}" % (p_name, p_para)
        else:
            return "{%s:%s:%s}" % (p_name, p_para, p_extra)

    def _generate_data(self, p_template):
        """
        分析模板
        :param p_template:
        :type p_template: str
        :return:
        """
        type_name, type_para, type_extra = ('', '', '')
        types = p_template.split(':')

        if 2 == len(types):
            type_name, type_para = types
        elif 3 == len(types):
            type_name, type_para, type_extra = types
        else:
            return '', p_template

        if 'DATE_STR' == type_name:
            return self._generate_date_str(type_para, type_extra)
        elif 'RANDOM' == type_name:
            return self._generate_random(type_para)
        elif 'INCREASE' == type_name:
            return self._generate_increase(type_para, type_extra)
        else:
            self._logger.error('Invalid data type')
            return '', p_template

    def _generate_date_str(self, p_para, p_extra=None):
        """
        产生日期字符串, DATA_STR:data:+|-n
        :return:
        """
        template_str = self._combine_template('DATE_STR', p_para, p_extra)
        date_extra = p_extra or 0

        try:
            delta = datetime.timedelta(days=int(date_extra))
        except (ValueError, TypeError):
            self._logger.error('Wrong template extra %s' % p_extra)
            return '', template_str

        time_today = datetime.datetime.now()
        time_today += delta

        result_data = time_today.strftime(p_para)

        return result_data, template_str

    def _generate_random(self, p_para):
        """
        生成随机数
        :param p_para: 参数,随机数长度
        :return:
        """
        result_data = str(OrcString.random_by_len(p_para))

        return result_data, self._combine_template('RANDOM', p_para)

    def _generate_increase(self, p_para, p_extra):
        """

        :return:
        """
        try:
            num_res = int(p_para)
            num_extra = int(p_extra)
        except (TypeError, ValueError):
            self._logger.error('Wrong increase parameter %s:%s' % (p_para, p_extra))
            return '', self._combine_template('INCREASE', p_extra, p_extra)

        num_res += num_extra

        result_data = str(num_res)
        result_template = self._combine_template('INCREASE', result_data, p_extra)

        return result_data, result_template

    def set_template(self, p_str):
        """
        设置初始模板字符串
        :param p_str:
        :return:
        """
        self._origin_str = p_str

    def get_data(self):
        """
        获取结果字符串
        :return:
        """
        self._split_template()

        for _index in range(len(self._temp_list)):
            if 1 == _index % 2:
                res, template = self._generate_data(self._temp_list[_index])

                self._result_list[_index] = res
                self._temp_list[_index] = template

        result_str = ''.join(self._result_list)
        temp_str = ''.join(self._temp_list)

        return result_str, temp_str

    @staticmethod
    def static_get_data(p_str):
        """
        静态方式获取数据
        :return:
        """
        user_def = UserDefStr()
        user_def.set_template(p_str)
        return user_def.get_data()
