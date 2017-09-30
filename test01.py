# coding=utf-8
# import json
#
# a = dict(a=1, b=2, c=3)
#
# b = json.dumps(a)
#
# print type(b)
#
# c = eval(b)
#
# print c
# print type(c)
#
#
#
#
#
#
#
# def select_ul(property, text1, text2):
#
#     top = property.find_element_by(property.type, property.value)
#
#     first_level = top.find_element_by_xpath('li[text=' + text1 + ']')
#
#     return first_level.find_element_by_xpath('li[text=' + text2 + ']')
#
#
# select_ul((driver, ID, 'id'), 'value1', 'value2')


# def create_diamond(num):
#
#     def create_star(_num):
#         return '* ' * ((_num - 1) / 2) + '*'
#
#     center = num + 1
#
#     for i in range(num):
#         print ' ' * (abs((i + 1) * 2 - center) / 2), create_star((center - abs((i + 1) * 2 - center)) - 1)
#
#
# create_diamond(11)

#
# def create(_length, _height, type=True):
#
#     def create_star(num, type=True):
#         return ('*' + ' ' * (num - 2) + '*') if type else '*' * num
#
#     for i in range(_height):
#         _type = not ((0 == i) or ((_height - 1) == i))
#         print ' ' * (_height - i) + create_star(_length, type and _type)
#
# create(16, 5, True)
# create(16, 5, False)
#
# from OrcLib.LibRunTime import OrcRunTime
#
#
# rtm = OrcRunTime('DRIVER')
#
# rtm.set_value('ABC', 'ABC')
import re

# class A:
#
#     def __init__(self):
#
#         self.a = 1
#         self.abc()
#
#     def abc(self):
#         print self.a
#
# class B(A):
#
#     def __init__(self):
#
#         A.__init__(self)
#
#     def abc(self):
#         self.a = 2
#         print self.a
#
#
# aaa = B()


# a = True
# if (a): print "OK"

# def read_data():
#     pass
#
#
# def login(parameter):
#     pass
#
#
# def fee(parameter):
#     pass
#
#
# def exit(parameter):
#     pass
#
#
# def search(parameter):
#     pass
#
#
# def execute(cmd):
#
#     parm = read_data()
#
#     if 'login' == cmd:
#         login(parm)
#     elif 'fee' == cmd:
#         fee(parm)
#     elif 'exit' == cmd:
#         exit(parm)
#     elif 'search' == cmd:
#         search(parm)
#     else:
#         pass
#
#
# def case_01():
#     execute('login')
#     execute('search')
#     execute('exit')
#
#
# def case_02():
#     execute('login')
#     execute('fee')
#     execute('exit')

# s = ['A', 'B', None, ' C', ' ']
# print [item for item in s if item and item.strip()]

# import time
# import multiprocessing
# from multiprocessing import queues
# from time import sleep
# from selenium import webdriver
#
#
# def my_get(driver, url, flag):
#     driver.get(url)
#     flag.put(True)
#
# root = webdriver.Firefox(executable_path='/Users/zhaojingping/PycharmProjects/AuxiTools/test/OrcTestToolsKit/driver/web/geckodriver')
#
# aflag = multiprocessing.Queue()
# p = multiprocessing.Process(target=my_get, args=(root, 'http://www.ch.com', aflag))
# p.start()
#
# for i in range(5):
#     try:
#         if aflag.get_nowait():
#             break
#     except queues.Empty:
#         pass
#
#     sleep(1)
# start_time = time.time()
# root.find_element_by_id('closeAdPop').click()
# print time.time() - start_time
#
#
# def get(p_driver, p_url, p_timeout):
#
#     def _get(_driver, _url, _flag):
#         _driver.get(_url)
#         _flag.put(True)
#
#     flag = multiprocessing.Queue()
#     p = multiprocessing.Process(target=_get, args=(root, 'http://www.ch.com', flag))
#     p.start()
#
#     for i in range(p_timeout):
#         try:
#             if aflag.get_nowait():
#                 break
#         except queues.Empty:
#             pass
#
#         sleep(1)
#
# from new import classobj

# from OrcLib.LibCmd import OrcCmd
# from OrcLib.LibCmd import OrcDriverCmd
# from OrcLib.LibCmd import WebCmd
# from OrcLib.LibType import WebObjectType
# from OrcLib.LibType import WebItemModeType
# from OrcLib.LibNet import OrcSocketResource
#
# cls_cmd = WebCmd()
# cls_cmd.set_cmd_type(WebObjectType.WIDGET)
# cls_cmd.set_cmd_object('330000028')  # id
# cls_cmd.set_cmd_operation('CONTEXT') # operation
# cls_cmd.set_mode(WebItemModeType.OPERATE)
# cls_cmd.set_data(["'abc'"])  # data
#
# command = OrcCmd()
#
# driver_command = OrcDriverCmd()
# driver_command.set_cmd(cls_cmd)
#
# command.set_cmd(driver_command)
#
# _resource = OrcSocketResource('Driver')
# _result = _resource.get(command.get_cmd_dict())
# print _result.status
# print _result.message
# print _result.data
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

root = webdriver.Chrome(executable_path='/Users/zhaojingping/PycharmProjects/AuxiTools/test/OrcTestToolsKit/driver/web/chromedriver-Darwin')
root.get('http://www.17sucai.com/pins/demoshow/15182')

time.sleep(5)
frame = root.find_element_by_id('iframe-wrap').find_element_by_tag_name('iframe')
root.switch_to.frame(frame)
widget = root.find_element_by_id('demo1Box')
# menu = root.find_element_by_id('clientMenu').find_element_by_xpath('li[1]/a[1]')
# root.context("abcde")
ActionChains(root).context_click(widget).perform()
time.sleep(3)
root.close()
