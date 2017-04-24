# coding=utf-8
import socket
import json

from datetime import datetime
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from OrcLib.LibProgram import orc_singleton
from OrcLib.LibProgram import OrcFactory
from OrcLib.LibProgram import OrcSocketServer
from OrcLib.LibCommon import OrcCovert
from OrcLib.LibLog import OrcLog

Base = declarative_base()


class RunTime(Base):
    """
    Table tab_run_time
    """
    __tablename__ = 'tab_run_time'

    id = Column(Integer, autoincrement=True, primary_key=True)
    module = Column(String(16))
    data_flag = Column(String(16))
    data_index = Column(Integer)
    data_value = Column(String(128))

    def __init__(self, p_def=None):

        if p_def is None:
            return

        field = OrcFactory.create_dict(p_def)

        self.id = field.value('id')
        self.module = field.value('module')
        self.data_flag = field.value('data_flag')
        self.data_index = field.value('data_index')
        self.data_value = field.value('data_value')

    def __repr__(self):
        return "<RunTime(id='%s', module='%s', data_flag='%s')>" % \
               (self.id, self.module, self.data_flag)

    def to_json(self):

        return dict(
            id=self.id,
            module=self.module,
            data_flag=self.data_flag,
            data_index=self.data_index,
            data_value=self.data_value
        )


class RunData(Base):
    """
    Data table
    """
    __tablename__ = 'tab_data'

    id = Column(Integer, primary_key=True)
    test_env = Column(String(16))
    src_id = Column(Integer)
    src_type = Column(String(16))
    step_order = Column(Integer)
    data_flag = Column(String(32))
    data_order = Column(Integer)
    data_type = Column(String(16))
    data_mode = Column(String(16))
    data_value = Column(String(128))
    comment = Column(String(512))
    create_time = Column(DateTime, default=datetime.now())
    modify_time = Column(DateTime, default=datetime.now())

    def __init__(self, p_def=None):

        if p_def is None:
            return

        field = OrcFactory.create_dict(p_def)

        self.id = field.value('id')
        self.test_env = field.value('test_env')
        self.src_id = field.value('src_id')
        self.src_type = field.value('src_type')
        self.step_order = field.value('step_order')
        self.data_flag = field.value('data_flag')
        self.data_order = field.value('data_order')
        self.data_type = field.value('data_type')
        self.data_mode = field.value('data_mode')
        self.data_value = field.value('data_value')
        self.comment = field.value('comment')
        self.create_time = OrcCovert.str2time(field.value('create_time'))
        self.modify_time = OrcCovert.str2time(field.value('modify_time'))

    def __repr__(self):
        return "<RunTime(id='%s', data_flag='%s')>" % (self.id, self.data_flag)

    def to_json(self):

        return dict(
            id=self.id,
            test_env=self.test_env,
            src_id=self.src_id,
            src_type=self.src_type,
            step_order=self.step_order,
            data_flag=self.data_flag,
            data_order=self.data_order,
            data_type=self.data_type,
            data_mode=self.data_mode,
            data_value=self.data_value,
            comment=self.comment,
            create_time=self.create_time,
            modify_time=self.modify_time
        )


@orc_singleton
class MemDB(object):
    """

    """
    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog('resource.mem_db')

        # 初始化数据库连接:
        self.__engine = create_engine('sqlite:///:memory:')

        # 建表
        Base.metadata.create_all(self.__engine)

        # 创建DBSession类型:
        self.create_session = sessionmaker(bind=self.__engine)


class RunTimeDB(object):
    """
    实时数据
    """
    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog('resource.mem_db.run_time_db')

        self._db = MemDB()

    def db_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        self.__logger.info('%s input: %s' % (self.db_add.__name__, p_data))

        result = True
        session = self._db.create_session()

        try:
            session.add(RunTime(p_data))
            session.commit()

        except exc.IntegrityError, err:
            session.rollback()
            result = False
            self.__logger.error("add error: %s" % err)

        finally:
            session.close()

        self.__logger.info('%s result: %s' % (self.db_add.__name__, result))

        return result

    def db_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        self.__logger.info('%s input: %s' % (self.db_delete.__name__, p_id))

        result = True
        session = self._db.create_session()

        try:
            _item = session.query(RunTime).filter_by(id=p_id)
            session.delete(_item)
            session.commit()

        except exc.IntegrityError, err:
            result = False
            session.rollback()
            self.__logger.error("delete error: %s" % err)

        finally:
            session.close()

        self.__logger.info('%s result: %s' % (self.db_delete.__name__, result))

        return result

    def db_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        self.__logger.info('%s input: %s' % (self.db_update.__name__, p_data))

        if 'id' not in p_data:
            return False

        result = True
        session = self._db.create_session()
        item_id = p_data['id']

        try:
            _item = session.query(RunTime).filter_by(id=item_id)
            _field = OrcFactory.create_dict(p_data)

            _item.module = _field.value('', _item.module)
            _item.data_flag = _field.value('', _item.data_flag)
            _item.data_index = _field.value('', _item.data_index)
            _item.data_value = _field.value('', _item.data_value)

            session.commit()

        except exc.IntegrityError, err:
            result = False
            session.rollback()
            self.__logger.error("update error: %s" % err)

        finally:
            session.close()

        self.__logger.info('%s result: %s' % (self.db_update.__name__, result))

        return result

    def db_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        self.__logger.info('%s input: %s' % (self.db_search.__name__, p_cond))

        result = list()
        session = self._db.create_session()

        try:
            result = session.query(RunTime)

            if 'module' in p_cond:
                result = result.filter_by(module=p_cond['module'])

            if 'data_flag' in p_cond:
                result = result.filter_by(data_flag=p_cond['data_flag'])

            if 'data_index' in p_cond:
                result = result.filter_by(data_index=p_cond['data_index'])

            result = result.all()

        except exc.IntegrityError, err:
            self.__logger.error("search error: %s" % err)

        finally:
            session.close()

        result = [item.to_json() for item in result]

        self.__logger.info('%s result: %s' % (self.db_search.__name__, result))

        return result


class RunDataDB(object):
    """
    运行数据
    """
    def __init__(self):

        object.__init__(self)

        self.__logger = OrcLog('resource.mem_db.run_data_db')

        self._db = MemDB()

    def db_add(self, p_data):
        """
        新增
        :param p_data:
        :return:
        """
        self.__logger.info('%s input: %s' % (self.db_add.__name__, p_data))

        result = True
        session = self._db.create_session()

        try:
            session.add(RunData(p_data))
            session.commit()

        except exc.IntegrityError, err:
            result = False
            session.rollback()
            self.__logger.error("add error: %s" % err)

        finally:
            session.close()

        self.__logger.info('%s result: %s' % (self.db_add.__name__, result))

        return result

    def db_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        self.__logger.info('%s input: %s' % (self.db_delete.__name__, p_id))

        result = True
        session = self._db.create_session()

        try:
            _item = session.query(RunData).filter_by(id=p_id)
            session.delete(_item)
            session.commit()

        except exc.IntegrityError, err:
            result = False
            session.rollback()
            self.__logger.error("delete error: %s" % err)

        finally:
            session.close()

        self.__logger.info('%s result: %s' % (self.db_delete.__name__, result))

        return result

    def db_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        self.__logger.info('%s input: %s' % (self.db_update.__name__, p_data))

        if 'id' not in p_data:
            return False

        result = True
        session = self._db.create_session()

        item_id = p_data['id']

        try:
            _item = session.query(RunData).filter_by(id=item_id)
            _field = OrcFactory.create_dict(p_data)

            _item.test_env = _field.value('', _item.test_env)
            _item.src_id = _field.value('', _item.src_id)
            _item.src_type = _field.value('', _item.src_type)
            _item.step_order = _field.value('', _item.step_order)
            _item.data_flag = _field.value('', _item.data_flag)
            _item.data_order = _field.value('', _item.data_order)
            _item.data_type = _field.value('', _item.data_type)
            _item.data_mode = _field.value('', _item.data_mode)
            _item.data_value = _field.value('', _item.data_value)
            _item.comment = _field.value('', _item.comment)

            session.commit()

        except exc.IntegrityError, err:
            result = False
            session.rollback()
            self.__logger.error("update error: %s" % err)

        finally:
            session.close()

        self.__logger.info('%s result: %s' % (self.db_update.__name__, result))

    def db_search(self, p_cond):
        """
        查询
        :param p_cond:
        :return:
        """
        self.__logger.info('%s input: %s' % (self.db_search.__name__, p_cond))

        result = list()
        session = self._db.create_session()

        try:
            result = session.query(RunTime)

            if 'test_env' in p_cond:
                result = result.filter_by(test_env=p_cond['test_env'])

            if 'src_id' in p_cond:
                result = result.filter_by(src_id=p_cond['src_id'])

            if 'src_type' in p_cond:
                result = result.filter_by(test_env=p_cond['test_env'])

            if 'step_order' in p_cond:
                result = result.filter_by(step_order=p_cond['step_order'])

            if 'data_flag' in p_cond:
                result = result.filter_by(data_flag=p_cond['data_flag'])

            if 'data_order' in p_cond:
                result = result.filter_by(data_order=p_cond['data_order'])

            if 'data_type' in p_cond:
                result = result.filter_by(data_type=p_cond['data_type'])

            if 'data_mode' in p_cond:
                result = result.filter_by(data_mode=p_cond['data_mode'])

            result = result.all()

        except exc.IntegrityError, err:
            self.__logger.error("search error: %s" % err)

        result = [item.to_json for item in result]

        self.__logger.info('%s result: %s' % (self.db_search.__name__, result))

        return result


# class MemServer(object):
#
#     def __init__(self, p_ip, p_port):
#
#         self._logger = OrcLog('resource.mem_db.mem_server')
#
#         self._ip = p_ip
#         self._port = p_port
#
#         self.__db_run_time = RunTimeDB()
#         self.__db_run_data = RunDataDB()
#
#     def start(self):
#
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         sock.bind((self._ip, self._port))
#         sock.listen(1)
#
#         while True:
#
#             connection, address = sock.accept()
#
#             try:
#                 connection.settimeout(5)
#
#                 _cmd = connection.recv(1024)
#
#                 self._logger.info('%s input: %s' % (self.start.__name__, _cmd))
#
#                 # 多进程不起作用,暂时用单进程
#                 # task = multiprocessing.Process(target=self.execute, args=(_cmd,))
#                 # result = task.start()
#                 # task.join()
#                 result = self.execute(_cmd)
#
#                 if "quit" == result:
#                     break
#
#                 self._logger.info('%s result: %s' % (self.start.__name__, result))
#
#                 connection.send(str(result))
#
#             except socket.timeout:
#                 self._logger.error("time out")
#                 connection.send(str(False))
#
#             except Exception, err:
#                 self._logger.error(err)
#                 connection.send(str(False))
#
#             connection.close()
#
#     def execute(self, p_cmd):
#         """
#
#         :param p_cmd:
#         :return:
#         """
#         self._logger.info('%s input: %s' % (self.execute.__name__, p_cmd))
#
#         _data = json.loads(p_cmd)
#         _tab = None if 'TABLE' not in _data else _data['TABLE']
#         _cmd = None if 'CMD' not in _data else _data['CMD']
#         _para = None if 'PARA' not in _data else _data['PARA']
#
#         if 'quit' == _cmd:
#             return _cmd
#
#         if 'RunTime' == _tab:
#             db = RunTimeDB()
#         elif 'RunData' == _tab:
#             db = self.__db_run_data
#         else:
#             return list()
#
#         result = OrcFactory.create_switch(dict(
#             ADD=db.db_add,
#             DELETE=db.db_delete,
#             UPDATE=db.db_update,
#             SEARCH=db.db_search)).run(_cmd, _para)
#
#         self._logger.info('%s result: %s' % (self.execute.__name__, result))
#
#         return result

class MemServer(OrcSocketServer):

    def __init__(self, p_ip, p_port):

        OrcSocketServer.__init__(self, p_ip, p_port)

        self._logger = OrcLog('resource.mem_db.mem_server')

        self.__db_run_time = RunTimeDB()
        self.__db_run_data = RunDataDB()

    def execute(self, p_cmd):
        """
        执行
        :param p_cmd:
        :return:
        """
        self._logger.info('%s input: %s' % (self.execute.__name__, p_cmd))

        _data = json.loads(p_cmd)
        _tab = None if 'TABLE' not in _data else _data['TABLE']
        _cmd = None if 'CMD' not in _data else _data['CMD']
        _para = None if 'PARA' not in _data else _data['PARA']

        if 'quit' == _cmd:
            return _cmd

        if 'RunTime' == _tab:
            db = RunTimeDB()
        elif 'RunData' == _tab:
            db = self.__db_run_data
        else:
            return list()

        result = OrcFactory.create_switch(dict(
            ADD=db.db_add,
            DELETE=db.db_delete,
            UPDATE=db.db_update,
            SEARCH=db.db_search)).run(_cmd, _para)

        self._logger.info('%s result: %s' % (self.execute.__name__, result))

        return result
