# coding=utf-8
import re
from OrcLib import get_config


class DataSrcMod(object):
    """

    """
    def __init__(self):

        object.__init__(self)

        self._configer = get_config('data_src')

    def usr_add(self, p_data):
        """
        新增, 增加两个配置项一个用于记录数据源,一个用于记录对应于环境的数据库信息
        :param p_data:{[ID], env, para}
        :return:
        """
        if not isinstance(p_data, dict):
            return dict()

        db_data = p_data.copy()

        # 获取 ID
        if 'id' in db_data:
            src_id = db_data['id']

        else:
            ids = [int(item) for item in self._configer.get_sections() if not re.search('\.', item)]

            if ids:
                src_id = str(max(ids) + 1)
            else:
                src_id = '1'

        db_id = None
        if 'env' in p_data and p_data['env']:
            db_id = "%s.%s" % (src_id, db_data['env'])

        # 增加 section
        self._configer.add_section(src_id)

        if db_id:
            self._configer.add_section(db_id)

        # 写入数据
        for _key, _value in db_data.items():

            # 通用信息写入数据源配置项
            if _key in ('name', 'desc'):
                self._configer.set_option(src_id, _key, _value)

            # 其他信息写入数据库信息配置
            elif (_key not in ('env', 'id')) and db_id:
                self._configer.set_option(db_id, _key, _value)

            # 环境/id信息在section中体现,不再写入
            else:
                continue

        return p_data

    def usr_delete(self, p_id):
        """
        删除
        :param p_id:
        :return:
        """
        ids = [item for item in self._configer.get_sections()
               if ((item == p_id) or re.match("^%s\..*" % p_id, item))]

        for _id in ids:
            self._configer.del_section(_id)

        return True

    def usr_update(self, p_data):
        """
        更新
        :param p_data:
        :return:
        """
        if not isinstance(p_data, dict):
            return False

        db_data = p_data.copy()

        src_id = str(p_data['id'])
        db_id = None if 'env' not in db_data else "%s.%s" % (src_id, db_data['env'])

        if src_id not in self._configer.get_sections():
            return False

        # 如果配置项不存在,则新建一个
        if (db_id is not None) and (db_id not in self._configer.get_sections()):
            self._configer.add_section(db_id)

        # 删除现有配置项
        self._configer.del_section(db_id)
        self._configer.add_section(db_id)

        # 更新
        for _key, _value in db_data.items():

            if _key in ('id', 'env'):
                continue

            # 通用信息写入数据源配置项
            if _key in ('name', 'desc'):
                self._configer.set_option(src_id, _key, _value)

            # 其他信息写入数据库信息配置
            elif (_key not in ('env', 'id')) and (db_id is not None):
                self._configer.set_option(db_id, _key, _value)

            # 环境/id信息在section中体现,不再写入
            else:
                continue

        return True

    def usr_search(self, p_cond=None):
        """
        查询
        :param p_cond:
        :return:
        """
        if not isinstance(p_cond, dict):
            return list()

        section = None if 'id' not in p_cond else p_cond['id']

        if section is None:

            data_list = list()

            for _section in self._configer.get_sections():
                # 文件为空时有缺陷

                if not re.search('\.', _section):
                    data_list.extend(self.usr_search(dict(id=_section)))

            return data_list

        else:
            conf = dict(id=section)

            sections = self._configer.get_options(section)

            if sections is None:
                return []

            for _section in self._configer.get_options(section):
                conf[_section] = self._configer.get_option(section, _section)

            return [conf]

