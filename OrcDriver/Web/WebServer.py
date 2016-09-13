# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from service import DriverService

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import orc_invoke


class DriverSelenium:

    def __init__(self):

        self.logger = OrcLog("driver.selenium")
        self.__service = DriverService()

        self.__browser = "FIREFOX"  # 浏览器
        self.__env = "TEST"  # 环境

        self.__window = None  # 当前窗口
        self.__root = None  # 根节点

        self.__objects = {}  # 存储出现过的对象

    def run(self):
        pass

    def set_browser(self, p_browser):
        """
        Set test browser
        :param p_browser:
        :return:
        """
        self.__browser = p_browser

    def set_env(self, p_env):
        """
        Set environment
        :param p_env:
        :return:
        """
        self.__env = p_env

    def open_page(self, p_page_id):
        """
        Return a selenium object of page or frame
        :param p_page_id: page_id
        :return: NodeDef
        """
        _para = dict(page_id=p_page_id, page_env=self.__env)
        _url = self.__service.page_get_url(_para)

        if self.__root is None:

            try:

                if "IE" == self.__browser:
                    self.__root = webdriver.Ie()
                elif "FIREFOX" == self.__browser:
                    self.__root = webdriver.Firefox()
                elif "CHROME" == self.__browser:
                    self.__root = webdriver.Chrome()
                else:
                    pass

                self.__root.get(_url)

            except WebDriverException, err:

                self.__root = None

    def get_widget(self, p_object_id):
        """
        Get a selenium object of widget
        :param p_object_id:
        :return: NodeDef
        """
        # if self.__root is None:
        #     return None

        _para_def = dict(id=p_object_id)
        _path_def = orc_invoke(self.__interface["usr_get_def"], _para_def)
        _widget = self.__root

        # noinspection PyTypeChecker
        for t_def in _path_def:

            _para_det = dict(widget_id=t_def["id"])
            _path_det = orc_invoke(self.__interface["usr_get_det"], _para_det)

            _type = t_def["widget_type"]
            _flag = t_def["widget_flag"]

            if "FRAME" == _type:

                pass

                # _widget.switch_to_default_content()
                # _widget.switch_to.frame(self.__get_object(_path_det, _widget))

            elif "WINDOW" == _type:

                pass

                # i_current_window = self.__window
                # if _flag != self.__window:
                #
                #     self.__window = _flag
                #     i_founded = False
                #     i_current_handle = _widget.current_window_handle
                #
                #     all_handles = _widget.window_handles
                #     for handle in all_handles:
                #
                #         if handle != i_current_handle:
                #             _widget.switch_to_window(handle)
                #             self.__root.switch_to_window(handle)
                #
                #             # i_founded = self.check_object(self.get_item_definition(t_def['ID'])[0]['ATTR'])
                #             if i_founded:
                #                 break
                #
                #     if not i_founded:
                #         self.__window = i_current_window
                #         # raise OrcStepErrorException

            else:
                _widget = self.__get_object(_path_det, _widget)

        return _widget

    # def get_item_definition(self, p_item_id):
    #     """
    #     Get object definition of page or widget
    #     :param p_item_id:
    #     :return: NodDef
    #     """
        # res_value = []
        #
        # sql_str = "SELECT item_id, def_type, def_attr, def_desc" \
        #           "  FROM obj_define" \
        #           " WHERE item_id = '%s'" \
        #           "ORDER BY def_order" % \
        #           p_item_id
        #
        # tmp_value = self._database.get_all(sql_str)
        # # if tmp_value is None:
        #     # raise OrcObjectNotFound
        #
        # tmp_name = ["ID", "TYPE", "ATTR", "DESC"]
        # for ind_i in range(len(tmp_value)):
        #     res_value.append(dict((name, value) for name, value in zip(tmp_name, tmp_value[ind_i])))
        #
        # return res_value

    # def get_widget_path(self, p_item_flag):
    #     """
    #     Get a object tree of page or widget
    #     获取对象树，包括页面和控件
    #     :rtype : object
    #     :param p_item_flag: 对象 ID
    #     :return: PAGE tuple(page_id, page_type)
    #               ITEM tuple(page_id, item_flag, item_type)
    #     :raises: OrcParameterError 参数错误
    #               OrcWrongFlgException flg 错误
    #               OrcObjectNotFound 对象未找到
    #     """
    #     item_flag = p_item_flag  # 对象 ID
    #     sup_exists = True
    #     res_value = []
    #
    #     while sup_exists:
    #
    #         tmp_value = self.get_item_info(item_flag)
    #         res_value.append(tmp_value)
    #
    #         item_flag = get_parent_no(item_flag)
    #         if item_flag is None:
    #             sup_exists = False
    #
    #     return res_value
    #
    # def get_item_info(self, p_item_flag):
    #     """
    #     Get item info
    #     :param p_item_flag:
    #     :return:
    #     """
    #     item_flag = p_item_flag  # 对象 ID
    #     tmp_name = ['ID', 'FLAG', 'TYPE', 'DESC']
    #
    #     sql_str = "SELECT item_id, item_flag, item_type, item_desc" \
    #               "  FROM obj_items" \
    #               " WHERE item_flag = '%s'" % \
    #               item_flag
    #
    #     tmp_value = self._database.get_one(sql_str)
    #     # if tmp_value is None:
    #     #     raise OrcObjectNotFound
    #
    #     res_value = dict((name, value) for name, value in zip(tmp_name, tmp_value))
    #
    #     return res_value

    def __get_object(self, p_def_list, p_sup):
        """
        获取对象,调用 selenium 函数
        :rtype : object
        :param p_def_list: [[type,flg],....]
        :param p_sup:
        :return:
        """
        obj = p_sup
        def_list = p_def_list

        if 0 != len(p_def_list):

            obj_type = p_def_list[0]['TYPE']
            obj_attr = p_def_list[0]['ATTR']

            if "ID" == obj_type:
                # obj = obj.find_element_by_id(obj_attr)
                print 1
            elif "NAME" == obj_type:
                # obj = obj.find_element_by_name(obj_attr)
                print 2
            elif "TAG_NAME" == obj_type:
                # obj = obj.find_element_by_tag_name(obj_attr)
                print 3
            elif "XPATH" == obj_type:
                # obj = obj.find_element_by_xpath(obj_attr)
                print 4

            def_list.pop(0)
            # obj = self.__get_object(p_def_list, obj)

        return obj

    def check_object(self, p_item, p_time=20):
        """
        加载判断函数，加载页面直至 p_item_id 控件出现
        :param p_item: item_id, page, time
        :param p_time:
        :return:
        """
        i_displayed = True

        def chk_item(dr, _item):
            return self.get_item(_item)

        try:
            WebDriverWait(self.__root, p_time).until(lambda sup: chk_item(sup, p_item).is_displayed())
        except WebDriverException:
            i_displayed = False

        return i_displayed

    def save_screen(self, p_file):
        time.sleep(0.5)
        self.__root.save_screenshot(p_file)
