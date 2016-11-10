# coding=utf-8
import os
import re
from OrcLib import get_config
from OrcLib.LibNet import OrcInvoke
from RunCore import RunCore


class RunDefModel:
    """
    运行列表管理,操作目录,目录名为 [类型]_[id],目录内含有 result.res 的属于执行过的, result.res 是一个xml文件
    """

    def __init__(self):

        self.__config = get_config()
        self.__invoker = OrcInvoke()

        # Get url from configuration
        _url = get_config("interface").get_option("DRIVER", "url")
        self.__url = lambda _mod, _id: "%s/api/1.0/%s/%s" % (_url, _mod, _id)

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
                _batch = self.__invoker.get(self.__url("BatchDef", _id))
                _flag = _batch["batch_no"] if _batch is not None else ""
            else:
                _case = self.__invoker.get(self.__url("CaseDef", _id))
                _flag = _case["case_path"] if _case is not None else ""

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

    def usr_add(self, p_cond):
        """
        增加执行目录时 p_test=false, 为 true 时生成结果文件
        :param p_cond: {id, run_def_type, result}
        :return:
        :rtype: bool
        """
        _type = p_cond["run_def_type"]
        _id = p_cond["id"]
        _result = p_cond["result"] if "result" in p_cond else False

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

    def usr_update(self):
        """
        修改,暂无需求
        :return:
        """
        pass

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
        # except OSError:
        #     return False

        return True
