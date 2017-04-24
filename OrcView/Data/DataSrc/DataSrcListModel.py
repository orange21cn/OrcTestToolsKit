# coding=utf-8
from OrcLib import get_config
from OrcView.Lib.LibTable import ModelTable


class DataSrcListModel(ModelTable):
    """

    """
    def __init__(self):

        ModelTable.__init__(self, 'DataSrc')

        self.__configer = get_config('data_src')

    def service_add(self, p_data):
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

    def service_delete(self, p_list):
        """
        删除
        :param p_list:
        :return:
        """
        for _id in p_list:
            self.__configer.del_section(_id)

    def service_update(self, p_data):
        """
        更新
        :param p_data:
        :type p_data: dict
        :return:
        """
        db_data = p_data

        current_data = self.mod_get_current_data()
        if not current_data:
            return

        current_id = current_data['id']
        db_data["id"] = current_id

        cfg_data = self.__configer.get_options(current_id)
        for _key in cfg_data:
            self.__configer.del_option(current_id, _key)

        self.service_add(db_data)

    def service_search(self, p_data):
        """
        查询
        :param p_data:
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
