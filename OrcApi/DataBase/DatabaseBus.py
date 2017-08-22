# coding=utf-8
from OrcLib import LibCommon
from OrcLib.LibLog import OrcLog
from OrcLib.LibProgram import OrcFactory

LibCommon.set_default_encoding()

from .DataSrcBus import DataSrcBus


class DataBaseBus(object):

    def __init__(self):

        object.__init__(self)

        self._logger = OrcLog("driver.web.sql")

        # 资源
        self._bus_data_src = DataSrcBus()

    def bus_list_search(self, p_cond):
        """
        执行
        :param p_cond: TYPE:DEBUG|DATA
        :type p_cond: dict
        :return: select -- {FIELDS, DATA, TYPE},
        """
        # 查找数据源
        condition = OrcFactory.create_default_dict(p_cond)
        data_src = condition.value('DATA_SRC')
        data_sql = condition.value('SQL')
        data_type = condition.value('TYPE')

        result = self._bus_data_src.bus_search(data_src)

        db_info = OrcFactory.create_default_dict(result)
        db_type = db_info.value('type')

        if not db_info:
            return list()

        # 初始化数据驱动
        if 'SQLite' == db_type:
            from OrcApi.DataBase.DataBaseSQLite import DatabaseSqlite
            db = DatabaseSqlite(db_info.dict())

        elif 'MySql' == db_type:
            from OrcApi.DataBase.DataBaseMySql import DatabaseMySql
            db = DatabaseMySql(db_info.dict())

        elif 'Oracle' == db_type:
            from OrcApi.DataBase.DataBaseOracle import DatabaseOracle
            db = DatabaseOracle(db_info.dict())

        else:
            return list()

        db.db_init(data_src)

        # 执行 sql
        res_data = db.db_execute(data_sql)

        if 'DEBUG' == data_type:
            res_fields = db.db_fields(data_sql)
            return dict(FIELDS=res_fields, DATA=res_data)
        else:
            return res_data
