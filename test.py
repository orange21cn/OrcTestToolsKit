# coding=utf-8
import sys
import os
# _method = getattr(self, request.method.lower(), None)
#
# if _method is None and request.method == 'HEAD':
#     _method = getattr(self, 'get', None)

# return _method(*args, **kwargs)

import time

# print time.time()
# print time.localtime(1474157948.12)
# print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(752548048.12))
#
# # 474157948.12 1985-01-10 06:32:28
# # 473137948.12 1984-12-29 11:12:28
# # 533137948.12 1986-11-23 21:52:28
# # 613147948.12 1989-06-06 23:52:28
# # 633547948.12 1990-01-29 01:32:28
# # 602547948.12 1989-02-04 06:25:48
# # 742547948.12 1993-07-13 15:19:08
# # 752548048.12 1993-11-06 09:07:28
#
# abc = [1, 2, 3, 4]
# ddd = abc.reverse()
# print abc
# print ddd
#
# data = [474157948.12, 473137948.12, 533137948.12, 613147948.12,
#         633547948.12, 602547948.12, 742547948.12, 752548048.12]
#
# data_set = {time.strftime("%m", time.localtime(item)) for item in data}
# print data_set
from PySide.QtGui import QLabel
from PySide.QtGui import QApplication

OrcData = QApplication(sys.argv)

tp = QLabel()
tp.setWordWrap(True)
tp.setText("abcdefghijklmnopqrstuvwxyz" * 10)
tp.show()

OrcData.exec_()