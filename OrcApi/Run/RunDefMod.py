# coding=utf-8
import os
import re
from OrcLib import get_config
from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcResource
from OrcLib.LibNet import ResourceCheck
from RunData import RunData


class RunDefMod:
    """
    运行列表管理,操作目录,目录名为 [类型]_[id],目录内含有 result.res 的属于执行过的, result.res 是一个xml文件
    """
    def __init__(self):

        self.__config = get_config()
        self.__logger = OrcLog("resource.run.run_def.model")
        self.__resource_batch_def = OrcResource("BatchDef")
        self.__resource_case_def = OrcResource("CaseDef")

        self.__data = RunData()
        self.__home = self.__config.get_option("RUN", "home")

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
                _batch = self.__resource_batch_def.get(path=_id)

                # 检查结果
                ResourceCheck.result_status(_batch, u"查询计划信息", self.__logger)

                _flag = _id if not _batch.data else _batch.data["batch_no"]

            else:
                _case = self.__resource_case_def.get(path=_id)

                # 检查结果
                ResourceCheck.result_status(_case, u"查询计划信息", self.__logger)

                _flag = _id if not _case.data else _case.data["case_path"]

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
                _test_list = os.listdir(os.path.join(self.__home, _item))
                rtn.extend(list(
                    dict(id="%s:%s" % (_id, test), pid=_id, run_def_type="TEST", run_flag=test)
                    for test in _test_list))

        return rtn

    def usr_add(self, p_data):
        """
        增加执行目录 p_test=false, 为 true 时生成结果文件
        :param p_data: {id, run_def_type, result}
        :return:
        :rtype: bool
        """
        _type = p_data["run_def_type"]
        _id = p_data["id"]
        _result = p_data["result"] if "result" in p_data else False

        # 生成目录名称
        folder_root = os.path.join(self.__home, "%s_%s" % (_type, _id))

        # 建目录
        if not os.path.exists(folder_root):
            os.mkdir(folder_root)

        # 建执行结果文件
        if _result:

            from OrcLib.LibCommon import gen_date_str

            for _index in range(100):

                _flag = _index + 1

                if 10 > _flag:
                    _flag = "%s%s" % (0, _flag)

                res_folder = os.path.join(folder_root, "%s%s" % (gen_date_str(), _flag))
                res_file = os.path.join(res_folder, "default.res")

                if os.path.exists(res_folder):
                    continue

                os.mkdir(res_folder)

                self.__data.save_list(_type, _id, res_file)
                break

        return _id

    def usr_delete(self, p_list):
        """
        删除
        :param p_list:
        :type p_list: list
        :return:
        """
        delete_list = list()

        folder_info = {_name.split('_')[1]: _name for _name in os.listdir(self.__home)}

        for _item in p_list:
            _path = _item.split(':')

            if _path[0] in folder_info:

                _path[0] = folder_info[_path[0]]

                del_folder = self.__home
                for _folder in _path:
                    del_folder = os.path.join(del_folder, _folder)

                delete_list.append(del_folder)

        for _item in delete_list:

            if os.path.exists(_item):
                import shutil
                shutil.rmtree(_item)

        return True
