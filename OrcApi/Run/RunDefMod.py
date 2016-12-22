# coding=utf-8
import os
import re
from OrcLib import get_config
from OrcLib.LibNet import OrcHttpResource
from RunCore import RunCore


class RunDefMod:
    """
    运行列表管理,操作目录,目录名为 [类型]_[id],目录内含有 result.res 的属于执行过的, result.res 是一个xml文件
    """

    def __init__(self):

        self.__config = get_config()
        self.__resource_batch_def = OrcHttpResource("BatchDef")
        self.__resource_case_def = OrcHttpResource("CaseDef")

        self.__list = RunCore()
        self.__home = self.__list.get_home()

        if not os.path.exists(self.__home):
            os.mkdir(self.__home)

    def usr_search(self, p_cond=None):
        """
        查询列表
        :param p_cond: 条件 [id="", run_def_type=""]
        :return:
        """
        run_list = os.listdir(self.__home)
        rtn = list()

        # 条件匹配
        for _item in run_list:

            _status = True
            _type, _id = _item.split("_")

            # 查找 flag, batch 为 batch_no, case 为 case path
            if "BATCH" == _type:
                self.__resource_batch_def.set_path(_id)
                _batch = self.__resource_batch_def.get()
                _flag = _id if not _batch else _batch["batch_no"]

            else:
                self.__resource_case_def.set_path(_id)
                _case = self.__resource_case_def.get()
                _flag = _id if not _case else _case["case_path"]

            # 有条件时进行查找,无条件使使用全部数据
            if p_cond is not None:

                # 匹配 flag
                if "run_flag" in p_cond and not re.search(p_cond["run_flag"], _flag):
                    _status = False

                # 匹配 type
                if "run_def_type" in p_cond and _type != p_cond["run_def_type"]:
                    _status = False

            if _status:
                # 加入当前目录
                rtn.append(dict(id=_id, pid=None, run_def_type=_type, run_flag=_flag))

                # 加入目录下测试项
                _test_list = os.listdir("%s/%s" % (self.__home, _item))
                rtn.extend(list(
                    dict(id=test, pid=_id, run_def_type="TEST", run_flag=test)
                    for test in _test_list))

        return rtn

    def usr_add(self, p_data):
        """
        增加执行目录时 p_test=false, 为 true 时生成结果文件
        :param p_data: {id, run_def_type, result}
        :return:
        :rtype: bool
        """
        _type = p_data["run_def_type"]
        _id = p_data["id"]
        _result = p_data["result"] if "result" in p_data else False

        # 生成目录名称
        folder_root = "%s/%s_%s" % (self.__home, _type, _id)

        # 建目录
        if not os.path.exists(folder_root):
            os.mkdir(folder_root)

        # 建执行结果文件
        if _result:

            from OrcLib.LibCommon import gen_date_str

            res_folder = "%s/%s" % (folder_root, gen_date_str())
            res_file = "%s/default.res" % res_folder

            if not os.path.exists(res_folder):
                os.mkdir(res_folder)

            self.__list.search_list(_type, _id)

            self.__list.save_list(res_file)

        return _id

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :type p_list: list
        :return:
        """
        delete_list = []

        for _group in os.listdir(self.__home):
            _id = _group.split("_")[1]

            if _id in p_list:
                delete_list.append(_group)

            for _item in os.listdir("%s/%s" % (self.__home, _group)):

                if _item in p_list:
                    delete_list.append("%s/%s" % (_group, _item))

        # try:
        for _item in delete_list:
            _folder = "%s/%s" % (self.__home, _item)
            if os.path.exists(_folder):
                import shutil
                shutil.rmtree(_folder)

        return True
