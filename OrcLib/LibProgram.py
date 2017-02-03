# coding=utf-8


def orc_singleton(cls, *args, **kw):
    """
    单例
    :param cls:
    :param args:
    :param kw:
    :return:
    """
    instances = {}

    def _singleton():

        if cls not in instances:
            instances[cls] = cls(*args, **kw)

        return instances[cls]

    return _singleton
