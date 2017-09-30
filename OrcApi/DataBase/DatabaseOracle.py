# coding=utf-8
import re
import cx_Oracle

from OrcLib.LibProgram import OrcFactory


class DatabaseOracle(object):

    def __init__(self, p_info):

        object.__init__(self)

        # 配置
        self._info = OrcFactory.create_default_dict(p_info)

        # 连接
        self._connection = None

        # 游标
        self._cursor = None

    def db_init(self, p_id):
        """
        初始化连接
        :param p_id:
        :return:
        """
        db_ip = self._info.value('ip')
        db_port = self._info.value('port')
        db_user = self._info.value('user')
        db_password = self._info.value('password')
        db_service = self._info.value('service')

        self._connection = cx_Oracle.connect(
            "%s/%s@%s:%s/%s" % (db_user, db_password, db_ip, db_port, db_service))

        self._cursor = self._connection.cursor()

    def db_close(self):
        """
        关闭连接
        :return:
        """
        if self._cursor:
            self._cursor.close()
        else:
            return

        if self._connection:
            self._connection.close()

        return

    def db_execute(self, p_sql):
        """
        执行 SQL
        :param p_sql:
        :return:
        """
        if not self._cursor:
            return list()

        try:
            self._cursor.execute(p_sql)
            return self._cursor.fetchall()
        except cx_Oracle.DatabaseError:
            return list()

    def db_test_connection(self):
        """
        测试连通
        :return:
        """
        return self._connection is None

    def db_fields(self, p_sql):
        """
        返回字段定义
        :param p_sql:
        :return:
        """
        fields = re.sub('.*select[ \t]*', '', p_sql, re.IGNORECASE)
        fields = re.sub('[ \t]+from[ \t]*', '', fields, re.IGNORECASE)

        table_name = re.sub('.*from[ \t]*', '', p_sql, re.IGNORECASE)
        table_name = re.sub('[ \t]+.*', '', table_name)
        table_name = re.sub(';', '', table_name)

        if '*' == fields:

            if self._cursor is None:
                return list()

            result = self.db_execute(
                "SELECT column_name"
                "  FROM user_tab_columns"
                " WHERE TABLE_NAME = '%s'" % table_name
            )

            fields = [col[0] for col in result]

        else:
            fields = fields.split(',')
            for _index in range(len(fields)):
                fields[_index] = re.sub('^[ \t]*', '', fields[_index])
                fields[_index] = re.sub('[ \t]*$', '', fields[_index])
                fields[_index] = re.sub('[ \t]+.*', '', fields[_index])

        return fields
