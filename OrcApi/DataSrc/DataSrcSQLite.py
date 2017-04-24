# coding=utf-8
import os
import re
import sqlite3

from OrcLib import get_config


class DataSrcSqlite(object):

    def __init__(self):

        object.__init__(self)

        self.__configer = get_config('data_src')

        self._conn = None
        self._cursor = None

    def db_init(self, p_id):
        """
        初始化连接
        :param p_id:
        :return:
        """
        _file = self.__configer.get_option(p_id, 'db_file')

        if os.path.exists(_file):
            self._conn = sqlite3.connect(_file)
            self._cursor = self._conn.cursor()

    def db_close(self):
        """
        关闭连接
        :return:
        """
        if self._cursor:
            self._cursor.close()

        if self._conn:
            self._conn.close()

    def db_execute(self, p_sql):
        """
        执行SQL
        :param p_sql:
        :return:
        """
        if not self._cursor:
            return list()

        try:
            self._cursor.execute(p_sql)
            return self._cursor.fetchall()
        except sqlite3.OperationalError:
            return list()

    def db_test_connection(self):
        """
        测试连通性
        :return:
        """
        return self._conn is not None

    def db_fields(self, p_sql):
        """
        通过sql获取字段定义
        :param p_sql:
        :return:
        """
        t_sql = str.lower(str(p_sql))

        fields = re.sub('.*select[ \t]*', '', t_sql)
        fields = re.sub('[ \t]+from.*', '', fields)

        table_name = re.sub('.*from[ \t]*', '', t_sql)
        table_name = re.sub('[ \t]+.*', '', table_name)
        table_name = re.sub(';', '', table_name)

        if '*' == fields:

            if self._cursor is None:
                return list()

            result = self._cursor.execute(
                'SELECT \"sql\" FROM sqlite_master WHERE type = \"table\" AND name = \"%s\";' % table_name)

            tab_ddl = result.fetchall()

            if tab_ddl:
                tab_ddl = tab_ddl[0][0]
            else:
                return list()

            fields = re.sub('\n', '', tab_ddl)
            fields = re.sub('^[^\(]*\([ \t]*', '', fields)
            fields = re.sub('[ \t]*\)[ \t]*$', '', fields)
            fields = fields.split(',')
            for _index in range(len(fields)):
                fields[_index] = re.sub('^[ \t]*', '', fields[_index])
                fields[_index] = re.sub('[ \t]+.*', '', fields[_index])

                if re.match('PRIMARY', fields[_index]):
                    fields.remove(fields[_index])

        else:
            fields = fields.split(',')
            for _index in range(len(fields)):
                fields[_index] = re.sub('^[ \t]*', '', fields[_index])
                fields[_index] = re.sub('[ \t]*$', '', fields[_index])
                fields[_index] = re.sub('.*[ \t]+', '', fields[_index])

        return fields
