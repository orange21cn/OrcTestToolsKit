# coding=utf-8
import os
import codecs

from OrcLib.LibCmd import OrcRecordCmd


# class RunLog:
#     """
#     1. Batch(Group)/Case(Group)建目录
#     2. Case建文件
#     3. Step 写步骤起始
#     4. Step Operate/Check 写命令串
#     5. Step Operate 有数据的写输入数据
#     6. Step Operate WEB 截图
#     6. Step Check 检查项有数据写输出数据
#     'status', 'flag', 'run_det_type', 'pid', 'id', 'desc'
#     """
#     def __init__(self):
#
#         self.__log_file = None
#         self.__home = None
#         self.__current_content = None
#         self.__run_folder = None
#
#     def set_list(self, p_home, p_list):
#
#         self.__home = p_home
#
#         # 清理 list, 在 step 和 item 下不建目录
#         path_list = []
#         for item in p_list:
#             if item["run_det_type"] in ("STEP", "ITEM"):
#                 continue
#
#             path_list.append(item)
#
#         # 运行目录
#         self.__run_folder = self.__home
#         for _folder in ["%s_%s" % (item["run_det_type"], item["flag"]) for item in path_list]:
#             self.__run_folder = os.path.join(self.__run_folder, _folder)
#
#         if not os.path.exists(self.__run_folder):
#             os.mkdir(self.__run_folder)
#
#         # log 文件, 确保只在 case 下建文件
#         self.__current_content = p_list[len(p_list) - 1]
#
#         if self.__current_content["run_det_type"] == 'CASE':
#             self.__log_file = codecs.open(os.path.join(self.__run_folder, "default.log"), "a+")
#         elif self.__current_content["run_det_type"] in ("STEP", "ITEM"):
#             self.__log_file = codecs.open(os.path.join(self.__run_folder, "default.log"), "a+")
#         else:
#             pass
#
#     def run_begin(self):
#
#         if self.__log_file is None:
#             return
#
#         run_flag = self.__current_content["run_det_type"]
#
#         if "STEP" == run_flag:
#             self.__log_file.write("---> Begin step %s %s ----\n" %
#                                   (self.__current_content["flag"], self.__current_content["desc"].encode('utf-8')))
#         elif "ITEM" == run_flag:
#             self.__log_file.write(
#                 u"  -> Item %s -- %s\n" % (self.__current_content["flag"], "abc"))
#         else:
#             pass
#
#     def run_end(self, p_status):
#
#         if self.__log_file is None:
#             return
#
#         run_flag = self.__current_content["run_det_type"]
#
#         if "STEP" == run_flag:
#             self.__log_file.write("<--- End step %s, status is %s ----\n" %
#                                   (self.__current_content["flag"], p_status))
#             self.__log_file.write("\n")
#         elif "ITEM" == run_flag:
#             self.__log_file.write("  <- Item %s's status is %s ----\n" %
#                                   (self.__current_content["flag"], p_status))
#         else:
#             pass
#
#     def data(self, p_msg):
#         self.__log_file.write("    %s\n" % p_msg)
#
#     def get_folder(self):
#         return self.__run_folder
#
#     def __del__(self):
#
#         if self.__log_file is not None:
#             self.__log_file.close()

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

        # log 文件
        self._log_file = None

    def set_case_folder(self, p_home):
        """
        设置 case,建立目录并生成log记录文件
        :param p_home:
        :return:
        """
        # 建立目录,及文件
        if not os.path.exists(p_home):
            os.mkdir(p_home)

        self._log_file = codecs.open(os.path.join(p_home, "default.log"), "a+")

    def run_begin(self, p_content):
        """
        记录开始
        :param p_content:
        :type p_content: OrcRecordCmd
        :return:
        """
        if self._log_file is None:
            return

        if p_content.is_step_type():
            self._log_file.write("---> Begin step %s %s ----\n" %
                                 (p_content.flag, p_content.desc.encode('utf-8')))
        elif p_content.is_item_type():
            self._log_file.write(
                u"  -> Item %s -- %s\n" % (p_content.flag, "abc"))
        else:
            pass

    def run_end(self, p_status):
        """
        记录结束
        :param p_status:
        :return:
        """
        if self._log_file is None:
            return

        self._log_file.write("  <- Status is %s ----\n" % p_status)

    def data(self, p_msg):
        """
        记录数据
        :param p_msg:
        :return:
        """
        self._log_file.write("    %s\n" % p_msg)

    def __del__(self):

        if self._log_file is not None:
            self._log_file.close()