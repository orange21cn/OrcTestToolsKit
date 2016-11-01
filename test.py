# coding=utf-8
import sys
import os


class ResBase:

    def __init__(self, p_id):

        self._a = 1

    def get(self, a=None, b=None):
        print a
        print b


class Ddd(ResBase):

    def __init__(self):

        ResBase.__init__(self, 3)

        self._a = 4

abc = Ddd()
print abc.a

        # _method = getattr(self, request.method.lower(), None)
        #
        # if _method is None and request.method == 'HEAD':
        #     _method = getattr(self, 'get', None)

        # return _method(*args, **kwargs)