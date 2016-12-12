# coding=utf-8
import os
import codecs


class RunLog:
    """
    1. Batch(Group)/Case(Group)建目录
    2. Case建文件
    3. Step 写步骤起始
    4. Step Operate/Check 写命令串
    5. Step Operate 有数据的写输入数据
    6. Step Operate WEB 截图
    6. Step Check 检查项有数据写输出数据
    'status', 'flag', 'run_det_type', 'pid', 'id', 'desc'
    """
    def __init__(self):

        self.__log_file = None
        self.__home = None
        self.__current_content = None
        self.__run_folder = None

    def set_list(self, p_home, p_list):

        self.__home = p_home

        # 清理 list, 在 step 和 item 下不建目录
        path_list = []
        for item in p_list:
            if item["run_det_type"] in ("STEP", "ITEM"):
                continue

            path_list.append(item)

        # path_list.reverse()

        # 运行目录
        self.__run_folder = "%s/%s" % \
                            (self.__home,
                             "/".join(["%s_%s" % (item["run_det_type"], item["flag"]) for item in path_list]))
        if not os.path.exists(self.__run_folder):
            os.mkdir(self.__run_folder)

        # log 文件, 确保只在 case 下建文件
        self.__current_content = p_list[len(p_list) - 1]

        if self.__current_content["run_det_type"] == 'CASE':
            self.__log_file = codecs.open("%s/default.log" % self.__run_folder, "a+")
        elif self.__current_content["run_det_type"] in ("STEP", "ITEM"):
            self.__log_file = codecs.open("%s/default.log" % self.__run_folder, "a+")
        else:
            pass

    def run_begin(self):

        if self.__log_file is None:
            return

        run_flag = self.__current_content["run_det_type"]

        if "STEP" == run_flag:
            self.__log_file.write("---> Begin step %s %s ----\n" %
                                  (self.__current_content["flag"], self.__current_content["desc"].encode('utf-8')))
        elif "ITEM" == run_flag:
            self.__log_file.write(
                u"  -> Item %s -- %s\n" % (self.__current_content["flag"], "abc"))
        else:
            pass

    def run_end(self, p_status):

        if self.__log_file is None:
            return

        run_flag = self.__current_content["run_det_type"]

        if "STEP" == run_flag:
            self.__log_file.write("<--- End step %s, status is %s ----\n" %
                                  (self.__current_content["flag"], p_status))
            self.__log_file.write("\n")
        elif "ITEM" == run_flag:
            self.__log_file.write("  <- Item %s's status is %s ----\n" %
                                  (self.__current_content["flag"], p_status))
        else:
            pass

    def data(self, p_msg):
        self.__log_file.write("    %s\n" % p_msg)

    def __del__(self):

        if self.__log_file is not None:
            self.__log_file.close()
