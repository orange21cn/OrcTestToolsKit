# coding=utf-8
from OrcLib import get_config


class DataSrcMod(object):

    def __init__(self):

        object.__init__(self)

        self.__configer = get_config('data_src')

    def usr_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        db_data = p_data

        # 获取 ID
        if 'id' in db_data:
            db_id = db_data['id']
            db_data.pop('id')
        else:
            ids = [int(item) for item in self.__configer.get_sections()]

            if ids:
                db_id = str(max(ids) + 1)
            else:
                db_id = '1'

            self.__configer.add_section(db_id)

        # 写入数据
        for _key, _value in db_data.items():
            self.__configer.set_option(db_id, _key, _value)

    def usr_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        self.__configer.del_section(p_id)

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        cfg_id = p_data['id']

        cfg_data = self.__configer.get_options(cfg_id)
        for _key in cfg_data:
            self.__configer.del_option(cfg_id, _key)

        self.usr_add(p_data)

    def usr_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        data_list = list()

        for _section in self.__configer.get_sections():

            # 文件为空时有缺陷,留一个 0 保证文件不为空
            # if '0' == _section:
            #     continue

            _name = self.__configer.get_option(_section, 'name')
            _desc = self.__configer.get_option(_section, 'desc')

            data_list.append(dict(
                id=_section,
                name=_name,
                desc=_desc
            ))

        return data_list

    def usr_execute(self, p_id, p_cmd):
        """
        执行
        :param p_id:
        :param p_cmd: {ID, SQL}
        :return: select -- {FIELDS, DATA}
        """
        cmd_id = str(p_id)
        cmd_sql = p_cmd['SQL']

        db_type = self.__configer.get_option(cmd_id, 'type')

        if not db_type:
            return list()

        if 'SQLite' == db_type:
            from .DataSrcSQLite import DataSrcSqlite
            db = DataSrcSqlite()

        elif 'MySql' == db_type:
            from .DataSrcMySql import DataSrcMySql
            db = DataSrcMySql(cmd_id)

        elif 'Oracle' == db_type:
            from .DataSrcOracle import DataSrcOracle
            db = DataSrcOracle(cmd_id)

        else:
            return list()

        db.db_init(cmd_id)

        res_fields = db.db_fields(cmd_sql)
        res_data = db.db_execute(cmd_sql)

        return dict(FIELDS=res_fields, DATA=res_data)
